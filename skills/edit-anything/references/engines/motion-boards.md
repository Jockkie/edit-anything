# YouTube AI Motion Graphics boards (Sirio Berati)

**What it is.** 74 animated explainer boards (1920 × 1080 HTML with GSAP: diagrams, charts, component motion, workflows, story boards) that sync to a voice, plus the prompts and three Claude skills (`explainer-board-brief`, `explainer-board-system`, `board-sync`). MIT.

**The method (nine steps).** References folder → find your style → the canvas in numbers (size, padding, the empty camera box, the end screen) → a `checks.md` where every correction becomes a DO or a DON'T and the AI checks every frame against it → templates → a skill with a board catalog tagged in the words you say → Whisper transcript word by word → sync every board to the voice → frame-exact export with Chrome and FFmpeg.

**What Edit Anything borrows as method.** The canvas in numbers, the `checks.md` learning file (`references/learning.md`), tagging boards by the words people say.

**Use it for.** Route C talking heads that need a board next to the face, and route B explainers with data.

**Note.** GSAP timelines are fine inside this engine because it syncs and exports frame-exact; outside it, keep to one clock.
