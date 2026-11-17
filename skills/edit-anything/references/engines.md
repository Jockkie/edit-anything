# Engines: which one for which scene

Edit Anything does not draw everything itself. It picks the engine that fits each scene, installs it only with the user's consent, and keeps every scene on one clock so the film can be retimed to a real voice. Each engine was studied for its method (what it does, what it needs, where it fails); those notes are in `references/engines/`. Engines are installed from their own repositories under their own licences; their code and style texts are not copied into this skill, except Explainer Studio, which ships with it.

## Choose by scene

| The scene needs | Engine | Licence | Notes file |
|-----------------|--------|---------|------------|
| An explainer look from a library, wide or reel, with its own sound kit | **Explainer Studio** (ships here) | MIT | `engines/explainer-studio.md` |
| A vertical reel from a post, page, video or product, cut to a voice, with a camera placeholder | html-reel (when installed) | the author's terms | `engines/html-reel.md` |
| A short film in a strong named style | Lemo-Opuscar (its own plugin) | code MIT, style texts CC BY-NC 4.0 | `engines/lemo-opuscar.md` |
| A product or launch promo from real screenshots | video-shotcraft (Remotion) | Apache 2.0 | `engines/video-shotcraft.md` |
| Charts, diagrams and boards next to a talking head | YouTube AI Motion Graphics boards | MIT | `engines/motion-boards.md` |
| Hand-drawn character animation | Claude Animation Base (p5.js, p5.brush) | MIT (the Clawd character is Anthropic's, not licensed) | `engines/claude-animation-base.md` |
| 3D scenes, physics, glow, depth | three.js with React Three Fiber, Rapier, postprocessing | MIT | `engines/three-r3f.md` |
| Real 3D modelling and renders | Blender over MCP (mcp-for-blender) | MIT | `engines/blender-mcp.md` |
| Pixel-art effects and game-like moments | pixelfx | MIT | `engines/pixelfx.md` |
| Realistic people, places or products in motion | Flora (Seedance, Kling, Veo and others), from an approved style frame | paid, per generation | `references/tools.md` |
| Sound effects made in code, listening and judging | earshot | MIT | `engines/earshot.md` |
| The beat grid of the music | librosa | ISC | `references/sound.md` |
| The editor timeline | DaVinci Resolve over MCP, or a file the editor opens | MIT (the MCP) | `references/handoff.md` |

## Rules for every engine

1. **One clock.** A scene is drawn as a pure function of time (`draw(t)` or `window.__frame(t)`), never by timers or CSS timelines that run at their own pace. Then a renderer can step it frame by frame and retime it to the real voice.
2. **Look.md drives it.** Palette, type and motion come from the style system, not from the engine's defaults.
3. **Contact sheet before render.** Render a strip of frames (every 0.5 s) and look at it before rendering the whole scene.
4. **Install with consent.** Say what you will install, how big it is and what it unlocks, then ask. Pin a release where the engine has one.
5. **Respect the licence.** Credit every engine in the delivery notes. Do not ship CC BY-NC material in anything the user sells. Never reproduce a third-party character or style text as the user's own.
6. **When an engine fails twice, step down.** Use a simpler engine for that scene (Explainer Studio covers most), and say so.
