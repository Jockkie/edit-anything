#!/usr/bin/env python3
"""Measured checks on a render: the outside judge for every delivery.

    python3 verify_export.py film.mp4 [--target social|broadcast|podcast] [--shape 9:16]
                             [--expect-seconds 30] [--transcript words.json --captions film.srt]
                             [--json] [--out report.json]

Uses ffprobe and ffmpeg (ebur128, blackdetect, freezedetect). Prints a pass or fail list and
exits 1 when any check fails. Every number comes from a measurement.
"""
import argparse
import json
import re
import subprocess
import sys

TARGETS = {"social": -14.0, "broadcast": -23.0, "podcast": -16.0}
TOLERANCE = {"social": 1.0, "broadcast": 0.5, "podcast": 1.0}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "json", path])
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or "ffprobe failed")
    data = json.loads(out.stdout)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    audio = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    return {"duration": float(data.get("format", {}).get("duration", 0) or 0), "video": video, "audio": audio}


def loudness(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-filter_complex", "ebur128=peak=true",
               "-f", "null", "-"]).stderr
    summary = err[err.rfind("Summary:"):] if "Summary:" in err else err
    i = re.search(r"I:\s+(-?[\d.]+|-inf)\s+LUFS", summary)
    p = re.search(r"Peak:\s+(-?[\d.]+|-inf)\s+dBFS", summary)
    val = lambda m: (float("-inf") if m.group(1) == "-inf" else float(m.group(1))) if m else None
    return val(i), val(p)


def spans(path, vf, key):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vf", vf, "-an", "-f", "null", "-"]).stderr
    if key == "black":
        return [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+)\s+black_end:([\d.]+)", err)]
    starts = [float(x) for x in re.findall(r"freeze_start:\s*([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"freeze_end:\s*([\d.]+)", err)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def words_of(text):
    return re.findall(r"[\w']+", text.lower())


def transcript_words(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return words_of(raw)
    if isinstance(data, dict):
        data = data.get("words") or data.get("segments") or data.get("text") or []
    if isinstance(data, str):
        return words_of(data)
    out = []
    for w in data:
        if isinstance(w, str):
            out += words_of(w)
        elif isinstance(w, dict):
            out += words_of(str(w.get("word") or w.get("text") or ""))
    return out


def srt_words(path):
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f.read().splitlines() if l.strip() and not l.strip().isdigit() and "-->" not in l]
    return words_of(" ".join(re.sub(r"<[^>]+>", "", l) for l in lines))


def in_order_share(reference, candidate):
    """Share of reference words that appear in the candidate in the same order (LCS / len)."""
    if not reference:
        return 1.0
    prev = [0] * (len(candidate) + 1)
    for r in reference:
        cur = [0]
        for j, c in enumerate(candidate, 1):
            cur.append(prev[j - 1] + 1 if r == c else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1] / len(reference)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--target", choices=sorted(TARGETS), default="social")
    ap.add_argument("--shape", help="expected shape, for example 9:16 or 16:9")
    ap.add_argument("--expect-seconds", type=float)
    ap.add_argument("--transcript")
    ap.add_argument("--captions")
    ap.add_argument("--max-black", type=float, default=0.3)
    ap.add_argument("--max-freeze", type=float, default=2.0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args(argv)

    checks = []
    def add(name, ok, detail):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    try:
        info = probe(a.file)
    except Exception as e:
        print(f"verify_export: error: {e}", file=sys.stderr)
        return 1

    v, au = info["video"], info["audio"]
    add("video stream", v is not None, f"{v['width']}x{v['height']}" if v else "no video stream")
    add("audio stream", au is not None, "present" if au else "no audio stream")
    if v and a.shape:
        w, h = (int(x) for x in a.shape.split(":"))
        ok = abs(v["width"] / v["height"] - w / h) < 0.01
        add("shape", ok, f"{v['width']}x{v['height']} against {a.shape}")
    if a.expect_seconds:
        diff = info["duration"] - a.expect_seconds
        add("length", abs(diff) <= 0.5, f"{info['duration']:.2f} s against {a.expect_seconds:.2f} s ({diff:+.2f} s)")
    else:
        add("length", info["duration"] > 0, f"{info['duration']:.2f} s")

    if au:
        lufs, peak = loudness(a.file)
        target, tol = TARGETS[a.target], TOLERANCE[a.target]
        add("integrated loudness", lufs is not None and abs(lufs - target) <= tol,
            f"{lufs:.1f} LUFS against {target:.0f} ±{tol:g}" if lufs is not None and lufs != float("-inf") else "silent or unreadable")
        add("true peak", peak is not None and peak <= -1.0,
            f"{peak:.1f} dBTP (at most -1.0)" if peak is not None and peak != float("-inf") else "unreadable")

    if v:
        black = [s for s in spans(a.file, f"blackdetect=d={a.max_black}:pix_th=0.10", "black")]
        add("black frames", not black,
            "none" if not black else "; ".join(f"{s:.2f}-{e:.2f} s" for s, e in black))
        frozen = spans(a.file, f"freezedetect=n=-60dB:d={a.max_freeze}", "freeze")
        add("frozen picture", not frozen,
            "none" if not frozen else "; ".join(f"from {s:.2f} s" for s, _ in frozen))

    if a.transcript and a.captions:
        ref, cap = transcript_words(a.transcript), srt_words(a.captions)
        share = in_order_share(ref, cap)
        add("captions match transcript", share >= 0.98, f"{share * 100:.1f}% of {len(ref)} words in order (at least 98%)")

    failed = [c for c in checks if not c["pass"]]
    report = {"file": a.file, "target": a.target, "passed": not failed, "checks": checks}
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    if a.json:
        print(json.dumps(report, indent=2))
    else:
        for c in checks:
            print(f"  {'pass' if c['pass'] else 'FAIL'}  {c['check']}: {c['detail']}")
        print(f"\n{len(checks) - len(failed)} of {len(checks)} checks pass" + ("" if not failed else ": fix the failures before delivery"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
