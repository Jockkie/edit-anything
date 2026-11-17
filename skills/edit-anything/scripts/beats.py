#!/usr/bin/env python3
"""Tempo and beat grid of a music file, for cutting on the beat.

    python3 beats.py music.wav [--out beats.json] [--bpm 120]

With librosa installed it tracks the beats in the audio. Without librosa, pass --bpm (and
optionally --offset, the time of the first beat in seconds) to get a fixed grid. The output
lists every beat and every bar start (four beats a bar unless --meter says otherwise).
"""
import argparse
import importlib.util
import json
import subprocess
import sys


def duration(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", path], capture_output=True, text=True, timeout=30)
        return float(out.stdout.strip())
    except Exception:
        return None


def track(path):
    import librosa  # optional dependency
    y, sr = librosa.load(path, mono=True)
    tempo, frames = librosa.beat.beat_track(y=y, sr=sr)
    times = librosa.frames_to_time(frames, sr=sr).tolist()
    tempo = float(tempo if not hasattr(tempo, "__len__") else tempo[0])
    return tempo, times, float(len(y) / sr), "librosa beat tracking"


def grid(bpm, offset, length):
    step = 60.0 / bpm
    times, t = [], offset
    while t <= length + 1e-9:
        times.append(round(t, 4))
        t += step
    return bpm, times, length, f"fixed grid at {bpm} BPM"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--bpm", type=float)
    ap.add_argument("--offset", type=float, default=0.0)
    ap.add_argument("--meter", type=int, default=4)
    ap.add_argument("--out")
    a = ap.parse_args(argv)

    if importlib.util.find_spec("librosa") and not a.bpm:
        tempo, beats, length, method = track(a.audio)
    else:
        if not a.bpm:
            print("beats.py: librosa is not installed; pass --bpm (and --offset) for a fixed grid, "
                  "or install it with: pip install librosa", file=sys.stderr)
            return 1
        length = duration(a.audio)
        if length is None:
            print("beats.py: could not read the length (is ffprobe installed?)", file=sys.stderr)
            return 1
        tempo, beats, length, method = grid(a.bpm, a.offset, length)

    bars = beats[::a.meter]
    result = {"file": a.audio, "method": method, "tempo_bpm": round(tempo, 2), "length_s": round(length, 3),
              "beats": [round(b, 3) for b in beats], "bar_starts": [round(b, 3) for b in bars]}
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
    print(f"{method}: {result['tempo_bpm']} BPM, {len(beats)} beats, {len(bars)} bars over {result['length_s']} s")
    print("First bar starts: " + ", ".join(f"{b:.2f}" for b in bars[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
