# Blender over MCP (mcp-for-blender)

**What it is.** An MCP server and Blender addon (MIT, by Siddharth Ahuja; formerly the PyPI package `blender-mcp`, now `mcp-for-blender`) that lets an agent model, build scenes and manipulate objects in Blender. Not made by Blender.

**Setup (with the user's consent).** `uvx mcp-for-blender setup` (installs the MCP for the user's clients and the addon), then open Blender; the addon starts its server when Blender opens. Fully quit and reopen the AI app after setup.

**The method for film.** Block out the scene, set materials and light from `Look.md`, animate with keyframes, render an image sequence (not an MP4) so frames can be checked and re-rendered one by one, then assemble with ffmpeg or hand the sequence to the editor.

**Use it for.** Real 3D renders: products, interiors, stylised worlds, title objects.

**Where it fails.** Long renders on a laptop (render a low-sample preview first), scenes the user cannot open later without Blender.
