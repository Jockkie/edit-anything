# earshot (ears for the agent)

**What it is.** A local tool that turns sound into evidence an agent can reason about (MIT, Leon Lin): what a file sounds like in words, how well it fits a description, the best moment in a recording, whether it reads as a real recording or as code-synthesized, a second-by-second listening transcript of a film, an annotated picture of it, and a scorecard against professional launch films. It also makes sounds in code and improves them by listening (`forge`), translates a recording into code (`fit`), and ships a bank of 252 effects made in code (`sfx`, `kit`). CLI, Python API and MCP server; runs on CPU; audio stays on the machine (except the optional `llm` command, only with the user's key and consent).

**Install (with consent).** `uv tool install "earshot[mcp] @ git+https://github.com/Leonxlnx/earshot"`, then `earshot doctor --fetch`, which downloads two open models (about 1.1 GB) once. Say the download size before installing. For more than a few calls, run it as an MCP server so the models stay loaded (first load 20 to 60 seconds).

**How Edit Anything uses it.**
- `earshot measure` for loudness, true peak and loudness range (no models needed).
- `earshot sfx` and `earshot kit` to give a code-made film its effects, each aimed at a cut with measured onset and peak; the `launch` preset mixes effects against the music bed.
- `earshot timeline FILE --video V` for sync of sound to picture cuts, and `earshot sheet` for an annotated picture an agent can read.
- `earshot critique` for a scorecard with timestamped fixes, before delivery.
- `earshot rank` and `find` to choose and trim effects or music from candidates.

**Rule.** Never say how something sounds without an earshot reading or a measurement, and quote the number.
