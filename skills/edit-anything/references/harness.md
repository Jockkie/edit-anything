# The harness: what the machine needs

Run `python3 scripts/harness_check.py` first. It looks for the tools below, prints what this machine can make now per route, and the one command that adds what is missing. It never prints keys; it only says whether a key is set.

| Tool | Needed for | Check | Install (ask first) |
|------|------------|-------|---------------------|
| ffmpeg and ffprobe | every route (export, measuring, cutting) | `ffmpeg -version` | macOS `brew install ffmpeg`; Windows `winget install ffmpeg`; Linux the package manager |
| Python 3.10+ | the scripts | `python3 --version` | python.org or the package manager |
| Node 18+ | code engines (Explainer Studio export, html-reel, shotcraft, three.js) | `node --version` | nodejs.org or `brew install node` |
| Chrome or Chromium | rendering code scenes frame by frame | the app or `chromium` | google.com/chrome |
| Whisper (any build) | transcripts with word times (routes C and D) | `whisper`, `whisper-cli`, `mlx_whisper` or MacWhisper | `pip install faster-whisper` or MacWhisper |
| librosa | the beat grid | `python3 -c "import librosa"` | `pip install librosa` |
| earshot | listening, effects, the sound scorecard | `earshot doctor` | `references/engines/earshot.md` |
| Blender | real 3D | the app | blender.org, then `references/engines/blender-mcp.md` |
| DaVinci Resolve | the timeline handoff over MCP | the app | blackmagicdesign.com, then `references/handoff.md` |
| A GPU | faster 3D and watercolour fills | the system report | none; step down to simpler looks without one |

Keys (only say whether they are set): `ELEVENLABS_API_KEY` for a voice, `GEMINI_API_KEY` for earshot's optional critique. Flora and Monid connect over MCP with their own sign-in.

## What each route needs at minimum

| Route | Minimum | Better with |
|-------|---------|-------------|
| A. Reel | ffmpeg, Node, Chrome | Whisper, librosa, earshot |
| B. Fully AI-made film | ffmpeg, Node, Chrome | Flora, Blender, earshot |
| C. Talking head in | ffmpeg, Whisper | librosa, earshot, the user's editor |
| D. Talking head to record | a phone, ffmpeg, Whisper | everything in C |

If a minimum tool is missing and the user does not want to install it, offer the route that works without it, or deliver the board and the build kit so the user can assemble in their own editor.
