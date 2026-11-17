# Security

Skills tell an AI agent what to do, and this one also runs scripts on your machine. Read this before you install, and review any skill before you enable it, from this repository or anywhere else.

## What runs, and what it can reach

| Part | What it does | Network | Writes files |
|------|--------------|---------|--------------|
| `skills/edit-anything/SKILL.md` and `references/` | Instructions and reference text for the agent | No | No |
| `skills/edit-anything/scripts/*.py` | Checks, measurements and handoff files (Python standard library; ffmpeg and ffprobe as external programs; librosa only if installed) | No | Only to the output path you or the agent pass on the command line |
| `hooks/check_reply.py` (Claude Code only) | Reads the current session transcript after each reply and can send the reply back for a fix | No | No |
| `engines/explainer-studio/studio.html` | A web page that draws the films; `render_studio.py` renders it headless and exports MP4 with ffmpeg | Loads fonts from Google Fonts | Only the MP4 at the `--out` path |
| `.mcp.json` / `mcp.json` | Registers the Flora and Monid MCP servers | Only after you authenticate them with `/mcp` | No |

- No script makes a network call. You can check this yourself: none of them imports a network library.
- Engines from other repositories (Lemo-Opuscar, video-shotcraft, Blender MCP, earshot, the DaVinci Resolve MCP and others) are installed only with your consent, from their own repositories, under their own licences and security policies. Review them before you enable them.
- Paid tools are never used without your consent, a quote and a spending cap you set. Footage, faces and voices are never sent to them without your consent for that file.

## Supported versions

Only the latest release receives fixes.

| Version | Supported |
|---------|-----------|
| 0.1.x | Yes |

## Reporting a vulnerability

Please do not open a public issue for a security problem: it shows everyone how to use the weakness before it is fixed.

Report it privately in this repository instead: go to the **Security** tab and choose **Report a vulnerability** ([direct link](https://github.com/Jockkie/edit-anything/security/advisories/new)). Only the maintainer and you can see the report. Describe:

- which script, hook or instruction is affected;
- how to reproduce it;
- what an attacker could do with it.

You will get a reply within seven days. Once a fix is released, the advisory is published and you are credited in it and in the changelog, unless you prefer not to be.

No GitHub account? Email **info@jockkie.com** with "Security" in the subject line.

Prompt-injection weaknesses count as security problems too: for example, a web page or document that makes the skill ignore its own rules, spend money without consent or send data to a tool.
