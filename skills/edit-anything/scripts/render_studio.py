#!/usr/bin/env python3
"""Render an Explainer Studio film to MP4, headless.

    python3 render_studio.py --look neon-sign-at-night --format reel --out film.mp4
    python3 render_studio.py --project project.json --look chalkboard --voice voice.wav --music bed.mp3 --out film.mp4
    python3 render_studio.py --list

Opens engines/explainer-studio/studio.html in headless Chromium, draws every
frame from the look's pure function of time, pipes the frames to ffmpeg and
mixes the synthesized effects, the voiceover and the music under the picture
(voice first, effects ducked under the voice, music ducked and faded, master
-14 LUFS for social by default, true peak -1.5 dBTP). Same t, same pixels: what you preview is what
you get.

Needs: ffmpeg, and Playwright for Python (pip install playwright, then
playwright install chromium), or Google Chrome installed.
No network calls except the Google Fonts the page loads for the look.
"""
import argparse
import array
import base64
import math
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STUDIO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "engines", "explainer-studio", "studio.html"))


def fail(msg, code=2):
    print(f"render_studio.py: {msg}", file=sys.stderr)
    sys.exit(code)


def mix(ffmpeg, tmp, video, out, seconds, effects, voice, music, lufs=-14.0):
    """The same mix the desktop app made, so the export sounds the same."""
    s = seconds
    pad = max(s, 4.0)  # loudnorm's 3 s window turns a clip of exactly 3 s into NaN; pad, then cut with -t
    prep = f"aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,apad=whole_dur={pad},atrim=0:{pad}"
    outro = f"apad=pad_dur=4,loudnorm=I={lufs}:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo[a]"
    fx_raw, fx_wav = os.path.join(tmp, "fx.f32"), os.path.join(tmp, "fx.wav")
    samples = array.array("f")
    samples.frombytes(effects[: len(effects) // 4 * 4])
    peak = 0.0
    for i, v in enumerate(samples):
        if not math.isfinite(v):
            samples[i] = 0.0
        elif abs(v) > peak:
            peak = abs(v)
    open(fx_raw, "wb").write(samples.tobytes())
    fx_norm = "loudnorm=I=-26:TP=-4:LRA=20" if peak > 1e-4 else "volume=1"  # loudnorm on silence gives NaN
    subprocess.run([ffmpeg, "-y", "-v", "error", "-f", "f32le", "-ar", "48000", "-ac", "2", "-i", fx_raw, fx_wav], check=True)
    inputs, n, vi, mi = ["-i", video], 1, -1, -1
    if voice:
        inputs += ["-i", voice]; vi = n; n += 1
    inputs += ["-i", fx_wav]; fi = n; n += 1
    if music:
        mh = os.path.join(tmp, "music_h.wav")
        subprocess.run([ffmpeg, "-y", "-v", "error", "-i", music, "-filter_complex",
                        "[0:a]asplit[a][b];[b]highpass=f=60,volume=30,asoftclip=type=tanh,highpass=f=150,lowpass=f=2500,volume=0.35[h];"
                        "[a][h]amix=inputs=2:normalize=0,alimiter=limit=0.9", mh], check=True)
        inputs += ["-i", mh]; mi = n; n += 1
    fade = f"afade=t=in:st=0:d=1.5,afade=t=out:st={max(0, s - 3.5)}:d=3.5"
    if vi > 0 and mi > 0:
        f = [f"[{vi}:a]{prep},loudnorm=I=-17:TP=-2,asplit=3[v1][v2][v3]",
             f"[{fi}:a]{prep},{fx_norm}[fx0]",
             "[fx0][v1]sidechaincompress=threshold=0.05:ratio=3:attack=10:release=250[fx]",
             f"[{mi}:a]{prep},{fade},loudnorm=I=-16:TP=-3:LRA=20,volume=0.4[mu0]",
             "[mu0][v3]sidechaincompress=threshold=0.08:ratio=2:attack=30:release=600[mu]",
             f"[v2][fx][mu]amix=inputs=3:normalize=0,{outro}"]
    elif vi > 0:
        f = [f"[{vi}:a]{prep},loudnorm=I=-17:TP=-2,asplit=2[v1][v2]",
             f"[{fi}:a]{prep},{fx_norm}[fx0]",
             "[fx0][v1]sidechaincompress=threshold=0.05:ratio=3:attack=10:release=250[fx]",
             f"[v2][fx]amix=inputs=2:normalize=0,{outro}"]
    elif mi > 0:
        f = [f"[{fi}:a]{prep},{fx_norm}[fx0]",
             f"[{mi}:a]{prep},{fade},loudnorm=I=-20:TP=-3:LRA=20[mu0]",
             f"[fx0][mu0]amix=inputs=2:normalize=0,{outro}"]
    else:
        solo = "loudnorm=I=-18:TP=-2" if peak > 1e-4 else "volume=1"
        f = [f"[{fi}:a]{prep},apad=pad_dur=4,{solo},aformat=sample_rates=48000:channel_layouts=stereo[a]"]
    r = subprocess.run([ffmpeg, "-y", "-v", "error", *inputs, "-filter_complex", ";".join(f), "-map", "0:v", "-map", "[a]",
                        "-c:v", "copy", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k", "-t", str(s),
                        "-movflags", "+faststart", out], capture_output=True, text=True)
    if r.returncode != 0:
        return "ffmpeg could not mix the sound: " + r.stderr[-300:]
    return None


def launch(p):
    try:
        return p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    except Exception:
        try:
            return p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required"])
        except Exception as e:
            fail("no Chromium found. Run: playwright install chromium (or install Google Chrome). " + str(e).splitlines()[0])


SHIM = """
window.studioApp = {
  begin: (o) => window.__py_begin(o),
  frame: async (buf) => { const b = new Uint8Array(buf); let s = ''; for (let i = 0; i < b.length; i += 32768) s += String.fromCharCode.apply(null, b.subarray(i, i + 32768)); return window.__py_frame(btoa(s)); },
  finish: async (o) => { const enc = (buf) => { if (!buf) return null; const b = new Uint8Array(buf); let s = ''; for (let i = 0; i < b.length; i += 32768) s += String.fromCharCode.apply(null, b.subarray(i, i + 32768)); return btoa(s); };
    return window.__py_finish({ effects: enc(o.effects), voice: enc(o.voice), music: enc(o.music), seconds: o.seconds }); },
  cancel: () => window.__py_cancel(),
};
"""


def main():
    ap = argparse.ArgumentParser(description="Render an Explainer Studio film to MP4, headless.")
    ap.add_argument("--look", help="look id, for example neon-sign-at-night (see --list)")
    ap.add_argument("--format", choices=["wide", "reel"], default="wide", help="wide 1280x720 or reel 1080x1920")
    ap.add_argument("--frame", help="reel frame around the picture, if the look offers one")
    ap.add_argument("--project", help="project JSON (beats and duration); default is the built-in demo")
    ap.add_argument("--seconds", type=float, help="render only this many seconds")
    ap.add_argument("--voice", help="voiceover file to mix under the picture")
    ap.add_argument("--music", help="music bed, ducked under the voice")
    ap.add_argument("--lufs", type=float, default=-14.0, help="master loudness: -14 for social (default), -16 for YouTube long form, -23 for broadcast")
    ap.add_argument("--out", help="output MP4")
    ap.add_argument("--looks", help="JSON list of extra looks (a brand's own style system), see engines/explainer-studio/README.md")
    ap.add_argument("--font", action="append", default=[], metavar="FAMILY=FILE", help="a local font file to use, for example Spectral=Spectral-Bold.ttf (repeat per weight)")
    ap.add_argument("--studio", default=DEFAULT_STUDIO, help="path to studio.html")
    ap.add_argument("--list", action="store_true", help="list the looks and stop")
    a = ap.parse_args()

    if not os.path.exists(a.studio):
        fail(f"studio.html not found at {a.studio}")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg and not a.list:
        fail("ffmpeg is not installed")
    if not a.list and not a.out:
        fail("--out is required")
    project = None
    if a.project:
        project = json.load(open(a.project, encoding="utf-8"))
        if not project.get("beats"):
            fail("the project needs a list of beats")
    for f in (a.voice, a.music):
        if f and not os.path.exists(f):
            fail(f"file not found: {f}")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        fail("Playwright is not installed. Run: pip install playwright && playwright install chromium")

    tmp = tempfile.mkdtemp(prefix="studio-")
    state = {}
    try:
        with sync_playwright() as p:
            browser = launch(p)
            page = browser.new_page(viewport={"width": 1560, "height": 980})
            page.add_init_script(SHIM)
            if a.looks:
                page.add_init_script("window.EXTRA_RECIPES = " + json.dumps(json.load(open(a.looks, encoding="utf-8"))) + ";")
            if a.font:
                css = []
                for spec in a.font:
                    fam, _, path = spec.partition("=")
                    if not os.path.exists(path):
                        fail(f"font file not found: {path}")
                    w = 400
                    for name, val in (("thin", 100), ("extralight", 200), ("light", 300), ("medium", 500), ("semibold", 600), ("extrabold", 800), ("black", 900), ("bold", 700)):
                        if name in os.path.basename(path).lower():
                            w = val
                            break
                    data = base64.b64encode(open(path, "rb").read()).decode()
                    css.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/ttf;base64,{data}) format('truetype');}}")
                page.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent=" + json.dumps("".join(css)) + ";document.head.appendChild(s);});")

            def begin(o):
                video = os.path.join(tmp, "video.mp4")
                state["video"] = video
                state["ff"] = subprocess.Popen([ffmpeg, "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(o["fps"]),
                                                "-c:v", "png", "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14",
                                                "-r", str(o["fps"]), video], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                state["frames"] = 0
                return os.path.abspath(a.out)

            def frame(b64):
                state["ff"].stdin.write(base64.b64decode(b64))
                state["frames"] += 1
                if state["frames"] % 60 == 0:
                    print(f"  frame {state['frames']}", file=sys.stderr)
                return True

            def finish(o):
                ff = state.pop("ff")
                ff.stdin.close()
                ff.wait()
                if ff.returncode != 0:
                    return {"error": "ffmpeg could not encode the frames: " + ff.stderr.read().decode()[-300:]}
                voice = a.voice
                if not voice and o.get("voice"):
                    voice = os.path.join(tmp, "voice.bin"); open(voice, "wb").write(base64.b64decode(o["voice"]))
                music = a.music
                if not music and o.get("music"):
                    music = os.path.join(tmp, "music.bin"); open(music, "wb").write(base64.b64decode(o["music"]))
                err = mix(ffmpeg, tmp, state["video"], os.path.abspath(a.out), o["seconds"], base64.b64decode(o["effects"]), voice, music, a.lufs)
                if err:
                    return {"error": err}
                return {"out": os.path.abspath(a.out), "bytes": os.path.getsize(a.out), "frames": state["frames"]}

            def cancel():
                ff = state.pop("ff", None)
                if ff:
                    ff.kill()
                return True

            page.expose_function("__py_begin", begin)
            page.expose_function("__py_frame", frame)
            page.expose_function("__py_finish", finish)
            page.expose_function("__py_cancel", cancel)
            page.goto("file://" + os.path.abspath(a.studio))
            page.wait_for_function("typeof window.__render === 'function' && window.CATALOG && window.CATALOG.length > 0", timeout=60000)
            if a.list:
                for look in page.evaluate("window.__looks()"):
                    print(f"{look['id']:<36} {look['family'] or ''}  {look['name']}")
                browser.close()
                return
            opts = {"style": a.look, "format": a.format, "frame": a.frame, "project": project, "seconds": a.seconds, "out": os.path.abspath(a.out)}
            r = page.evaluate("(o) => window.__render(o)", opts)
            browser.close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if not r or r.get("error"):
        fail((r or {}).get("error", "the render returned nothing"), 1)
    print(json.dumps({"out": r["out"], "bytes": r["bytes"], "frames": r.get("frames"), "look": a.look, "format": a.format}))
    print("Next: python3 verify_export.py " + r["out"] + " --target social --shape " + ("9:16" if a.format == "reel" else "16:9"), file=sys.stderr)


if __name__ == "__main__":
    main()
