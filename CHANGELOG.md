# Changelog

All notable changes to Edit Anything are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-11-17

First public release. Beta: built and checked with Claude; the scripts are tested, the full flow is new.

### Added

- **Edit Anything.** A mood-first interview with real references, four routes (reel, fully AI-made film, talking head in, talking head to record), a three-column script board (said, seen, lands on), a style system (`Look.md`), engine choice per scene, edit craft (paper edit, cuts on words, breaths and beats, retiming code scenes to a real voice), sound first, outside judges and a handoff to the user's own editor.
- **Explainer Studio** as the main engine, under MIT: 95 looks, wide or reel, a synthesized sound kit. One page, no app to install; `render_studio.py` renders it headless to MP4 with the sound mixed in.
- **Engine notes** for html-reel, Lemo-Opuscar, video-shotcraft, YouTube AI Motion Graphics, Claude Animation Base, three.js with React Three Fiber, Blender over MCP, pixelfx and earshot: method, needs and where each fails.
- **Scripts:** `render_studio.py` (Explainer Studio to MP4, headless), `harness_check.py` (what this machine can make), `beats.py` (beat grid), `verify_export.py` (loudness, true peak, black and frozen frames, length, shape, captions against the transcript), `handoff.py` (FCPXML, EDL, SRT and a mobile build kit for CapCut and Edits), `check_dossier.py` (gates and assumptions).
- **Trust layer.** Facts labelled seen, inferred or unknown; a visible self-check; a Claude Code guard hook.
- **Learning loop.** `checks.md` collects every correction, and after publishing the real numbers.
