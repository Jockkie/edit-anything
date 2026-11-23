# Explainer Studio

Short films in 95 looks, wide (16:9) or reel (9:16), with voiceover, sound and MP4 export. Made by Jockkie Studio; part of [Edit Anything](../../README.md) and its main engine for explainers and the animated layer over a talking head.

It ships as code: one page, `studio.html`, with the whole studio, the style library and the sound kit. Nothing to install to look at it.

## Preview

Open `studio.html` in a browser. Pick a look, choose wide or reel, load a voiceover, press play. Fonts load from Google Fonts, so the first open needs a connection.

## Render to MP4

```
pip install playwright && playwright install chromium
python3 ../../skills/edit-anything/scripts/render_studio.py --list
python3 ../../skills/edit-anything/scripts/render_studio.py --look neon-sign-at-night --format reel --voice voice.wav --out film.mp4
```

The script opens the page headless, draws every frame, pipes the frames to ffmpeg (H.264, CRF 14) and mixes the effects, the voiceover and an optional music bed under the picture: voice first, effects ducked under the voice, music ducked and faded, master at -14 LUFS for social (`--lufs -16` for YouTube long form). Use `--project project.json` for your own beats and timings, `--seconds` for a short test. Google Chrome works too when Chromium is not installed. ffmpeg is needed.

## How it works

- Every look is a pure function of time, `draw(ctx, W, H, t)`, on a 1280 × 720 logical canvas: the same `t` gives the same pixels, and randomness is seeded. That is what lets Edit Anything retime a scene to a real voice, and why the export matches the preview.
- A synthesized sound kit in plain Web Audio (pops, ticks, whooshes, risers, impacts, pen, chalk, brush and paper sounds). In voiceover mode the beds drop out and effects sit lower, so the voice stays on top.
- A project is JSON (beats and duration). Save it next to the script board to reuse it.
- In the 16-bit look the hero acts per beat: `act` is a pose (`idle`, `wave`, `point`, `cheer`, `think`, `present`) or a list of `{t, a}`; `walk` is `[from, to]` as a share of the width, with `walkFor` seconds; `hop` is a list of times he jumps. `enter` (`mosaic`, `swirl`, `iris`) sets the transition into a beat.
- Brand looks: `render_studio.py --looks looks.json --font Family=file.ttf` adds a brand's own palette, type and texture.
- The page exposes `window.__render(options)` and `window.__looks()` for headless use; `render_studio.py` supplies the frame and sound bridge as `window.studioApp`.

## Families

Popular Explainer Looks, Hand-Drawn, Illustration, Print, Dimensional (clay, voxel, isometric, wireframe), Retro Digital (16-bit, Amber CRT, CGA, Commodore 64, MacPaint, Phosphor Terminal, ZX Spectrum), Retro UI and Neon, and more.

## Licence

MIT, see [LICENSE](LICENSE). Fonts are loaded from Google Fonts under their own open licences.
