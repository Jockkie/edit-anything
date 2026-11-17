#!/usr/bin/env python3
"""What can this machine make? Looks for the tools Edit Anything uses and prints, per route,
what works now and the one command that adds what is missing. Never prints a key, only whether
it is set.

    python3 harness_check.py [--json]
"""
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys

MAC = sys.platform == "darwin"
WIN = sys.platform.startswith("win")


def version(cmd, args=("--version",)):
    path = shutil.which(cmd)
    if not path:
        return None
    try:
        out = subprocess.run([path, *args], capture_output=True, text=True, timeout=15)
        line = (out.stdout or out.stderr).strip().splitlines()
        return line[0][:80] if line else "found"
    except Exception:
        return "found"


def app(names):
    """Find a desktop app by name on macOS or Windows; on Linux look for a command."""
    for n in names:
        if MAC:
            for base in ("/Applications", os.path.expanduser("~/Applications")):
                if os.path.exists(os.path.join(base, n + ".app")):
                    return "found"
        elif WIN:
            for base in (os.environ.get("ProgramFiles", ""), os.environ.get("ProgramFiles(x86)", "")):
                if base and os.path.exists(os.path.join(base, n)):
                    return "found"
        if shutil.which(n.lower().replace(" ", "")):
            return "found"
    return None


def has_module(name):
    return importlib.util.find_spec(name) is not None


def install_hint(tool):
    hints = {
        "ffmpeg": "brew install ffmpeg" if MAC else ("winget install ffmpeg" if WIN else "sudo apt install ffmpeg"),
        "node": "brew install node" if MAC else ("winget install OpenJS.NodeJS" if WIN else "install Node 18+ from nodejs.org"),
        "chrome": "install Google Chrome from google.com/chrome",
        "whisper": "pip install faster-whisper   (or MacWhisper on a Mac)",
        "librosa": "pip install librosa",
        "earshot": 'uv tool install "earshot[mcp] @ git+https://github.com/Leonxlnx/earshot"',
        "blender": "install Blender from blender.org, then: uvx mcp-for-blender setup",
        "resolve": "install DaVinci Resolve (free) from blackmagicdesign.com",
    }
    return hints.get(tool, "")


def check():
    r = {"system": f"{platform.system()} {platform.machine()}", "python": sys.version.split()[0]}
    r["ffmpeg"] = version("ffmpeg", ("-version",))
    r["ffprobe"] = version("ffprobe", ("-version",))
    r["node"] = version("node")
    r["chrome"] = app(["Google Chrome", "Chromium"]) or version("google-chrome") or version("chromium")
    r["whisper"] = (version("whisper") or version("whisper-cli") or version("mlx_whisper")
                    or ("python module" if has_module("faster_whisper") or has_module("whisper") else None)
                    or app(["MacWhisper"]))
    r["librosa"] = "python module" if has_module("librosa") else None
    r["earshot"] = version("earshot") or ("python module" if has_module("earshot") else None)
    r["blender"] = app(["Blender"]) or version("blender")
    r["resolve"] = app(["DaVinci Resolve", "DaVinci Resolve Studio"])
    r["keys"] = {k: ("set" if os.environ.get(k) else "not set") for k in ("ELEVENLABS_API_KEY", "GEMINI_API_KEY")}
    return r


ROUTES = {
    "A. Reel": (["ffmpeg", "node", "chrome"], ["whisper", "librosa", "earshot"]),
    "B. Fully AI-made film": (["ffmpeg", "node", "chrome"], ["earshot", "blender"]),
    "C. Talking head in": (["ffmpeg", "whisper"], ["librosa", "earshot", "resolve"]),
    "D. Talking head to record": (["ffmpeg", "whisper"], ["librosa", "earshot", "resolve"]),
}


def main():
    r = check()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=2))
        return
    print(f"Machine: {r['system']}, Python {r['python']}\n")
    print("Tools:")
    for k in ("ffmpeg", "ffprobe", "node", "chrome", "whisper", "librosa", "earshot", "blender", "resolve"):
        print(f"  {'✓' if r[k] else '·'} {k:<8} {r[k] or 'not found'}")
    print("Keys: " + ", ".join(f"{k} {v}" for k, v in r["keys"].items()))
    print("\nWhat you can make now:")
    for route, (need, better) in ROUTES.items():
        missing = [t for t in need if not r[t]]
        extra = [t for t in better if not r[t]]
        if missing:
            print(f"  ✗ {route}: needs {', '.join(missing)}")
            for t in missing:
                print(f"      {t}: {install_hint(t)}")
        else:
            note = f" (better with {', '.join(extra)})" if extra else ""
            print(f"  ✓ {route}{note}")
    print("\nInstall nothing without asking the user first.")


if __name__ == "__main__":
    main()
