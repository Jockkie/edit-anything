# Explainer Studio

Short films in 95 looks, wide (16:9) or reel (9:16), with voiceover, sound and MP4 export. Made by Jockkie Studio; part of [Edit Anything](../../README.md) and its main engine for explainers and the animated layer over a talking head.

## Use it

**In a browser (preview):** open `studio.html`. Pick a look, choose wide or reel, load a voiceover, press play. Fonts load from Google Fonts, so the first open needs a connection.

**As a desktop app (export to MP4):**
```
npm install
npm start
```
`main.js` pipes the frames to the bundled ffmpeg (H.264, CRF 14) and puts the voiceover under the picture. `npm start -- --selftest` renders a short test film and reports the file size.

## How it works

- Every look is a pure function of time, `draw(ctx, W, H, t)`, on a 1280 × 720 logical canvas: the same `t` gives the same pixels, and randomness is seeded. That is what lets Edit Anything retime a scene to a real voice.
- A synthesized sound kit in plain Web Audio (pops, ticks, whooshes, risers, impacts, pen, chalk, brush and paper sounds). In voiceover mode the beds drop out and effects sit lower, so the voice stays on top. The same score renders live and offline, so the export matches the preview.
- A project is JSON (look, format, scenes, timings). Save it next to the script board to reuse it.

## Families

Popular Explainer Looks, Hand-Drawn, Illustration, Print, Dimensional (clay, voxel, isometric, wireframe), Retro Digital (16-bit, Amber CRT, CGA, Commodore 64, MacPaint, Phosphor Terminal, ZX Spectrum), Retro UI and Neon, and more.

## Licence

MIT, see [LICENSE](LICENSE). Fonts are loaded from Google Fonts under their own open licences.
