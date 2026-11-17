# Explainer Studio (ships with this skill)

**What it is.** Jockkie's own studio for short films in 95 looks, wide (16:9) or reel (9:16), with voiceover, a synthesized sound kit and MP4 export. Source in `engines/explainer-studio/studio.html` at the repository root: one page with the whole studio, the style library and the sound kit. No app to install.

**The method.**
- Every style is a pure function of time: `draw(ctx, W, H, t)` on a 1280 × 720 logical canvas. Same `t`, same pixels; randomness is seeded.
- A shared helper library (`H`): seeded random, gradient noise, easing, colour mixing, grain, paper texture, vignette.
- A sound kit in plain Web Audio (`SOUND.kit`): UI sounds (pop, tick, click, whoosh, swish, riser, thud, impact, stamp, ding, success, glitch, shutter) and hand-made media (pen, marker, chalk, pencil, brush strokes, paper, tape). In voiceover mode beds and music drop out, minor sounds play at about 60% and effects sit lower, so the voice stays on top. The same score renders live or offline, so the export matches the preview.
- A project is JSON: the style, the format, the scenes and the timings. Load a voiceover; the export puts it under the picture.
- Export: `scripts/render_studio.py` opens the page in headless Chromium, draws every frame, pipes the frames to ffmpeg (H.264, CRF 14, yuv420p) and mixes the effects, the voiceover and the music under the picture (master -14 LUFS for social by default). `--list` shows every look; `--project`, `--look`, `--format wide|reel`, `--voice`, `--music`, `--seconds` and `--lufs` set the rest.

**Use it for.** Explainers, reels, title cards, kinetic type, the animated layer over a talking head, any route A or B scene that fits one of the families: Popular Explainer Looks, Hand-Drawn, Illustration, Print, Dimensional, Retro Digital, Retro UI and Neon.

**Needs.** A browser to preview. To export: ffmpeg and Playwright for Python (`pip install playwright`, then `playwright install chromium`), or Google Chrome installed.

**Make it the user's.** Set the style's colours and fonts from `Look.md`; keep the motion. Save the project JSON next to the board so the next video reuses it.

**Where it fails.** Realistic people and places (use generated shots), very long films in one project (split per chapter), fonts that are not loaded before render (wait for `document.fonts.ready`).
