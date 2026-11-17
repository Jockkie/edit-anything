# Handoff: the user's own editor

The user picks the app they keep editing in. Edit Anything ends with something that app can open, so the user can change a cut, a title or the music themselves. Always deliver the MP4 too.

`python3 scripts/handoff.py edl.json --out handoff/ [--fcpxml] [--edl] [--srt] [--mobile-kit]` builds the files from the edit decision list (`templates/edit.json` → `edl`).

| Editor | What the user gets | How they open it |
|--------|--------------------|------------------|
| **DaVinci Resolve** (free or Studio) | A timeline built directly over MCP when the Resolve MCP is connected, otherwise an FCPXML file plus the media folder | MCP: it appears in the open project. File: File, Import, Timeline |
| **Final Cut Pro** | FCPXML plus the media folder | File, Import, XML |
| **Premiere Pro** | EDL (CMX 3600) plus the media folder; FCPXML also imports in recent versions | File, Import |
| **CapCut** | A mobile build kit: numbered clips in order, the voice, music and effect stems, an SRT, a cut list with times | Import the clips in order, add the stems, import the SRT as captions |
| **Edits (Instagram)** | The same mobile build kit; Edits imports clips and audio and adds captions itself | New project, import clips in order, add the audio |
| **No editor** | The MP4, the SRT and the stems | none needed |

CapCut and Edits cannot open project files made outside them, so the build kit is designed to rebuild the edit in a few minutes: the clip names start with their order and their start time, and the cut list says what goes where.

## DaVinci Resolve over MCP

Use the DaVinci Resolve MCP (samuelgursky/davinci-resolve-mcp, MIT) when the user has Resolve:
1. With consent, install it from its repository; it works with Resolve Studio through the official scripting API, and with the free edition through its in-app bridge (follow its README).
2. In Resolve, set Preferences, General, External scripting using to Local, and keep Resolve open.
3. Create a project and timeline, import the media, place the clips per the edit decision list, add the stems on their own tracks and the captions as a subtitle track.
4. Tell the user which tracks hold what, so they can change the music or a title themselves.

## What to tell the user at handoff

Two or three lines on what they may still want to adjust (for example "the music swell at 0:18 can come in a beat later if you prefer", "the title at 0:05 is a separate layer you can retype"), and where each part lives in their editor.
