<img src=".claude-plugin/icon.png" alt="" width="96" height="96">

# Edit Anything

*Part of [Jockkie Studio's open-source skills](https://github.com/Jockkie/jockkie-studio). I do the geeking. You get the easy part.*

> **Version 0.1.0, beta.** Built and checked with Claude; the scripts are tested, the full flow is new. See [Platform status](#platform-status), and please [report what you find](https://github.com/Jockkie/edit-anything/issues/new/choose).

An AI director and editor for people who have never edited a video, or have and got stuck. It finally gets the thing edited.

It starts where a good director starts: not with a form, but with references. You see a handful of looks and react ("this one feels like us", "not that"), and it turns your reactions into a brief. It checks what your computer can make, picks the route that fits what you already have, writes what is said and plans what is seen word by word, builds a style system that is yours, builds the scenes with the right open-source engine, cuts on words and beats with sound first, measures the result instead of guessing, and hands it over to the editor you already use, so you can keep changing it yourself.

## Four routes

| Route | When | You get |
|-------|------|---------|
| **Reel** | A short vertical video from an idea, a post, a page or a product | Script, voice, scenes, cut, captions |
| **Fully AI-made film** | No camera at all | Script, voice, scenes in code, generated shots only where code cannot, the edit |
| **Talking head in** | You already have takes | A transcript, a paper edit, cuts on words, pictures and titles on the right words, captions |
| **Talking head to record** | You will be on camera | A script in your own voice, a shot list for your phone, then the edit on your takes |

## What makes it different

- **Mood first.** References from Explainer Studio's 95 looks, Lemo-Opuscar's film styles, video-shotcraft's shots, motion-graphics boards and your own favourites. Your reactions become five mood axes: energy, temperature, texture, pace and type voice.
- **One board, three columns.** For every line: what is said, what is seen, and the word it lands on. You approve it before anything is rendered.
- **Edited like a pro.** A paper edit on the transcript, cuts on words and breaths, J and L cuts, the beat grid for music, captions from the transcript.
- **Sound first, and measured.** It cannot hear, so it measures: loudness and true peak with ffmpeg, and with [earshot](https://github.com/Leonxlnx/earshot) a listening transcript, effects placed against the cuts and a scorecard against professional launch films.
- **Outside judges.** Every render goes through `verify_export.py` (loudness, true peak, black and frozen frames, length, shape, captions against the transcript), and for a draft that matters two blind judges compare it with the previous one. A missed target with honest numbers beats a faked pass.
- **Your editor, your control.** A timeline for DaVinci Resolve (over MCP or FCPXML), Final Cut (FCPXML) or Premiere (EDL), or a build kit for CapCut and Edits: numbered clips, voice and music stems, an SRT and a cut list.
- **It learns.** Every correction becomes a line in `checks.md`, and after publishing the real numbers feed the next video.

## Engines

Edit Anything picks the engine per scene and installs it only with your consent. Each one was studied for its method; nothing is copied from repositories with other licences.

| Engine | For | Licence |
|--------|-----|---------|
| [Explainer Studio](engines/explainer-studio) (ships here, as code) | 95 looks, wide or reel, its own sound kit, rendered headless to MP4 | MIT |
| [html-reel](https://fil.design) (when installed) | Reels from a source, cut to a voice, with a camera placeholder | its author's terms |
| [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) | Films in 99 named styles | code MIT, style texts CC BY-NC 4.0 |
| [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | Product promos from real screenshots | Apache 2.0 |
| [YouTube AI Motion Graphics](https://github.com/sirioberati/YouTube-AI-Motion-Graphics) | Explainer boards synced to a voice | MIT |
| [Claude Animation Base](https://github.com/JohnHeibel/ClaudeAnimationBase) | Hand-drawn character animation | MIT |
| [three.js](https://github.com/mrdoob/three.js), [react-three-rapier](https://github.com/pmndrs/react-three-rapier), [react-postprocessing](https://github.com/pmndrs/react-postprocessing) | 3D, physics, effects | MIT |
| [Blender over MCP](https://github.com/ahujasid/mcp-for-blender) | Real 3D renders | MIT |
| [pixelfx](https://github.com/patch-gg/pixelfx) | Pixel-art effects | MIT |
| [earshot](https://github.com/Leonxlnx/earshot) | Listening, effects made in code, the sound scorecard | MIT |
| [librosa](https://github.com/librosa/librosa) | The beat grid | ISC |
| [DaVinci Resolve MCP](https://github.com/samuelgursky/davinci-resolve-mcp) | The timeline in your Resolve | MIT |

## Install

The skill folder is `skills/edit-anything`.

**Claude Code (plugin)**
```
/plugin marketplace add Jockkie/edit-anything
/plugin install edit-anything@edit-anything
```
All Jockkie Studio skills in one go: `/plugin marketplace add Jockkie/jockkie-studio`, then `/plugin install edit-anything@jockkie-studio`.

**Claude.ai**: zip the `skills/edit-anything` folder and upload it in Claude's skills settings. The scripts need a computer, so on Claude.ai you get the interview, the board and the plan.

**Hermes Agent**: this repository is also an [Agent Plugins](https://vercel.com/kb/guide/agent-plugins) package. Copy it into `~/.hermes/plugins/edit-anything`, then `hermes plugins enable edit-anything`.

**Codex, Cursor, GitHub Copilot, Gemini CLI, OpenClaw, Grok and other Agent Skills clients**: copy `skills/edit-anything` into the client's skills directory.

Start by saying something like "turn this talk into three reels", "I need a 30-second video for my launch" or "edit my takes".

## Platform status

| Platform | Status | What that means |
|----------|--------|-----------------|
| Claude Code | Validated | Manifest and hook pass `claude plugin validate`; the scripts are tested |
| Claude.ai | Interview and board | No local scripts there; rendering needs a computer |
| Hermes, Codex, Cursor and others | Untested | Built to the Agent Skills and Agent Plugins formats |

## Optional tools

Everything works without paid tools. Where they help, always with your consent, a quote and a spending cap you set:

- **[Flora](https://refer.flora.ai/jock-oosterveer-htu6)**: shots code cannot draw honestly (Seedance, Kling, Veo), style frames, B-roll. MCP: `https://mcp.flora.ai/mcp`
- **[Monid](https://monid.ai?fpr=jockkie)**: facts and examples from the web. MCP: `https://mcp.monid.ai/v1`

**Disclosure:** the Flora and Monid links are affiliate links. Jockkie earns a commission when you create an account through them. The skill says so before it shares a link.

## How this skill keeps you from trusting a guess

1. **What you told me and what I assumed**, in every summary, with your own words next to every fact.
2. **A check before every gate**: `check_dossier.py` blocks the next step while the brief, the board or the handoff is incomplete.
3. **Measured, not guessed**: every number about a render comes from a measurement with the tool named.
4. **In Claude Code, a guard** that sends a reply back when it asks several questions at once or claims a file was saved when none was written.

## Privacy

Footage, faces, voices and transcripts stay on your machine. Nothing goes to an external tool without your consent for that file. No one's face or voice is generated or cloned without their consent.

## Quality

Every change runs the script tests and checks on GitHub (`.github/workflows/tests.yml`). What changed is in the [changelog](CHANGELOG.md). Want to help? Read [CONTRIBUTING](CONTRIBUTING.md). Found a security problem? Report it privately through the Security tab ([how](SECURITY.md)).

## Credits

Explainer Studio by Jockkie Studio. The ambition method from Felix Rieseberg's "How to be more ambitious", as packaged in RoboNuggets' [be-ambitious](https://github.com/robonuggets/be-ambitious) (MIT). The retiming-by-word-anchors and camera-placeholder methods from html-reel (Meng To, fil.design). The checks-file method from Sirio Berati's YouTube AI Motion Graphics. Listening by earshot (Leon Lin). Every engine above under its own licence.

## The other skills

| Skill | For |
|-------|-----|
| [Consult Anything](https://github.com/Jockkie/consult-anything) | Owners and managers whose business is stuck |
| [Market This](https://github.com/Jockkie/market-this) | Owners and makers who need more customers |
| [Copywrite Me](https://github.com/Jockkie/copywrite-me) | Anyone who needs a text that sells |
| [Find My Ikigai](https://github.com/Jockkie/find-my-ikigai) | Anyone looking for what makes life worth living |
| [Align My Astro](https://github.com/Jockkie/align-my-astro) | Anyone who likes a daily reflection |

## Contact and support

- Website: https://www.jockkie.com
- Email: info@jockkie.com
- The skill is free. If it helped you: https://buymeacoffee.com/jockkie

## License

MIT
