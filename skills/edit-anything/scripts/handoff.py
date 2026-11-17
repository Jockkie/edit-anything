#!/usr/bin/env python3
"""Hand an edit over to the user's own editor.

    python3 handoff.py edl.json --out handoff/ [--fcpxml] [--edl] [--srt] [--mobile-kit [--render]]

Without format flags it writes all of them. The edit decision list (edl.json):

{
  "name": "Launch reel", "fps": 30, "width": 1080, "height": 1920,
  "clips": [{"file": "media/take1.mp4", "in": 2.0, "out": 5.5, "label": "hook"}],
  "audio": [{"file": "media/voice.wav", "start": 0.0, "role": "voice"},
            {"file": "media/music.wav", "start": 0.0, "role": "music", "in": 0.0, "out": 30.0}],
  "captions": [{"start": 0.0, "end": 1.4, "text": "Most people never finish a video."}]
}

Clips play one after another on the main track; audio items sit at their own start times.
FCPXML opens in Final Cut Pro and DaVinci Resolve, the CMX 3600 EDL in Premiere Pro and
Resolve, the SRT anywhere. The mobile kit (CapCut, Edits) is a cut list plus, with --render,
numbered clips cut by ffmpeg so they can be imported in order.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from fractions import Fraction
from xml.sax.saxutils import quoteattr


def frames(seconds, fps):
    return int(round(seconds * fps))


def rt(seconds, fps):
    """Rational time for FCPXML, on the frame grid."""
    n = frames(seconds, fps)
    f = Fraction(n, fps)
    return f"{f.numerator}/{f.denominator}s" if f.denominator != 1 else f"{f.numerator}s"


def tc(seconds, fps, hour=0):
    n = frames(seconds, fps) + hour * 3600 * fps
    ff = n % fps
    s = n // fps
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}:{ff:02d}"


def srt_time(seconds):
    ms = int(round(seconds * 1000))
    return f"{ms // 3600000:02d}:{(ms % 3600000) // 60000:02d}:{(ms % 60000) // 1000:02d},{ms % 1000:03d}"


def media_duration(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", path], capture_output=True, text=True, timeout=30)
        return float(out.stdout.strip())
    except Exception:
        return None


def validate(edl):
    problems = []
    if not edl.get("clips"):
        problems.append("no clips")
    for i, c in enumerate(edl.get("clips", []), 1):
        if "file" not in c or "in" not in c or "out" not in c:
            problems.append(f"clip {i}: needs file, in and out")
        elif c["out"] <= c["in"]:
            problems.append(f"clip {i}: out must be after in")
    for i, c in enumerate(edl.get("captions", []), 1):
        if c.get("end", 0) <= c.get("start", 0):
            problems.append(f"caption {i}: end must be after start")
    return problems


def write_srt(edl, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, c in enumerate(edl.get("captions", []), 1):
            f.write(f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c['text'].strip()}\n\n")


def write_edl(edl, path):
    fps = int(edl.get("fps", 30))
    rec = 0.0
    lines = [f"TITLE: {edl.get('name', 'Edit Anything')}", "FCM: NON-DROP FRAME", ""]
    for i, c in enumerate(edl["clips"], 1):
        length = c["out"] - c["in"]
        lines.append(f"{i:03d}  AX       V     C        {tc(c['in'], fps)} {tc(c['out'], fps)} "
                     f"{tc(rec, fps, 1)} {tc(rec + length, fps, 1)}")
        lines.append(f"* FROM CLIP NAME: {os.path.basename(c['file'])}")
        rec += length
    n = len(edl["clips"])
    for j, a in enumerate(edl.get("audio", []), 1):
        a_in, a_out = a.get("in", 0.0), a.get("out")
        if a_out is None:
            d = media_duration(a["file"])
            a_out = d if d else a_in
        lines.append(f"{n + j:03d}  AX       A{min(j + 1, 4)}    C        {tc(a_in, fps)} {tc(a_out, fps)} "
                     f"{tc(a['start'], fps, 1)} {tc(a['start'] + a_out - a_in, fps, 1)}")
        lines.append(f"* FROM CLIP NAME: {os.path.basename(a['file'])}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_fcpxml(edl, path, base):
    fps = int(edl.get("fps", 30))
    w, h = int(edl.get("width", 1920)), int(edl.get("height", 1080))
    files = []
    for c in edl["clips"] + edl.get("audio", []):
        if c["file"] not in files:
            files.append(c["file"])
    assets, ids = [], {}
    for k, fpath in enumerate(files, 1):
        ab = os.path.abspath(os.path.join(base, fpath))
        d = media_duration(ab)
        if d is None:
            d = max([c.get("out", 0) for c in edl["clips"] + edl.get("audio", []) if c["file"] == fpath] + [1.0])
        is_audio = any(a["file"] == fpath for a in edl.get("audio", [])) and not any(c["file"] == fpath for c in edl["clips"])
        ids[fpath] = f"a{k}"
        assets.append(f'    <asset id="a{k}" name={quoteattr(os.path.basename(fpath))} start="0s" duration="{rt(d, fps)}" '
                      f'hasVideo="{0 if is_audio else 1}" hasAudio="1" format="r1">'
                      f'<media-rep kind="original-media" src={quoteattr("file://" + ab)}/></asset>')
    total = sum(c["out"] - c["in"] for c in edl["clips"])
    spine, rec = [], 0.0
    first = edl["clips"][0]
    connected = []
    for j, a in enumerate(edl.get("audio", []), 1):
        a_in = a.get("in", 0.0)
        a_out = a.get("out") or (media_duration(os.path.join(base, a["file"])) or total)
        offset = first["in"] + a["start"]  # connected clips use the parent's own time
        connected.append(f'        <asset-clip ref="{ids[a["file"]]}" lane="-{j}" offset="{rt(offset, fps)}" '
                         f'start="{rt(a_in, fps)}" duration="{rt(a_out - a_in, fps)}" '
                         f'name={quoteattr(a.get("role", "audio"))} audioRole="{"dialogue" if a.get("role") == "voice" else "music"}"/>')
    for i, c in enumerate(edl["clips"]):
        length = c["out"] - c["in"]
        open_tag = (f'      <asset-clip ref="{ids[c["file"]]}" offset="{rt(rec, fps)}" start="{rt(c["in"], fps)}" '
                    f'duration="{rt(length, fps)}" name={quoteattr(c.get("label") or os.path.basename(c["file"]))}')
        if i == 0 and connected:
            spine.append(open_tag + ">")
            spine += connected
            spine.append("      </asset-clip>")
        else:
            spine.append(open_tag + "/>")
        rec += length
    doc = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.9">
  <resources>
    <format id="r1" frameDuration="1/{fps}s" width="{w}" height="{h}"/>
{chr(10).join(assets)}
  </resources>
  <library>
    <event name={quoteattr(edl.get('name', 'Edit Anything'))}>
      <project name={quoteattr(edl.get('name', 'Edit Anything'))}>
        <sequence format="r1" duration="{rt(total, fps)}" tcStart="0s" tcFormat="NDF">
          <spine>
{chr(10).join('    ' + s for s in spine)}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)


def write_mobile_kit(edl, out, base, render):
    kit = os.path.join(out, "mobile-kit")
    os.makedirs(kit, exist_ok=True)
    rows, rec = [], 0.0
    for i, c in enumerate(edl["clips"], 1):
        length = c["out"] - c["in"]
        label = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in (c.get("label") or "clip"))[:24]
        name = f"{i:02d}_{rec:06.2f}s_{label}.mp4"
        rows.append((i, name, rec, length, c["file"], c["in"], c["out"]))
        if render:
            src = os.path.join(base, c["file"])
            r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{c['in']:.3f}", "-i", src, "-t", f"{length:.3f}",
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
                                os.path.join(kit, name)], capture_output=True, text=True)
            if r.returncode != 0:
                print(f"handoff: could not cut clip {i}: {r.stderr.strip()[:200]}", file=sys.stderr)
        rec += length
    for a in edl.get("audio", []):
        src = os.path.join(base, a["file"])
        if render and os.path.exists(src):
            shutil.copy(src, os.path.join(kit, f"audio_{a.get('role', 'audio')}_{os.path.basename(a['file'])}"))
    write_srt(edl, os.path.join(kit, "captions.srt"))
    with open(os.path.join(kit, "CUT-LIST.md"), "w", encoding="utf-8") as f:
        f.write(f"# Cut list: {edl.get('name', 'Edit Anything')}\n\n")
        f.write("Import the clips in this order, add the audio files on their own tracks at their start time, "
                "then import captions.srt as captions.\n\n| # | Clip | Starts at | Length | From | Source in | Source out |\n"
                "|---|------|-----------|--------|------|-----------|------------|\n")
        for i, name, start, length, src, cin, cout in rows:
            f.write(f"| {i} | {name} | {start:.2f} s | {length:.2f} s | {os.path.basename(src)} | {cin:.2f} | {cout:.2f} |\n")
        if edl.get("audio"):
            f.write("\n| Audio | Role | Starts at |\n|-------|------|-----------|\n")
            for a in edl["audio"]:
                f.write(f"| {os.path.basename(a['file'])} | {a.get('role', 'audio')} | {a['start']:.2f} s |\n")
    return kit


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("edl")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fcpxml", action="store_true")
    ap.add_argument("--edl", dest="edl_out", action="store_true")
    ap.add_argument("--srt", action="store_true")
    ap.add_argument("--mobile-kit", action="store_true")
    ap.add_argument("--render", action="store_true", help="cut numbered clips with ffmpeg for the mobile kit")
    a = ap.parse_args(argv)

    with open(a.edl, encoding="utf-8") as f:
        edl = json.load(f)
    problems = validate(edl)
    if problems:
        print("handoff: error: " + "; ".join(problems), file=sys.stderr)
        return 1
    base = os.path.dirname(os.path.abspath(a.edl))
    os.makedirs(a.out, exist_ok=True)
    everything = not (a.fcpxml or a.edl_out or a.srt or a.mobile_kit)
    written = []
    if a.fcpxml or everything:
        p = os.path.join(a.out, "timeline.fcpxml"); write_fcpxml(edl, p, base); written.append(p)
    if a.edl_out or everything:
        p = os.path.join(a.out, "timeline.edl"); write_edl(edl, p); written.append(p)
    if a.srt or everything:
        p = os.path.join(a.out, "captions.srt"); write_srt(edl, p); written.append(p)
    if a.mobile_kit or everything:
        written.append(write_mobile_kit(edl, a.out, base, a.render))
    for p in written:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
