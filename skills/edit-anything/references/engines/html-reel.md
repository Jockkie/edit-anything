# html-reel (when installed)

**What it is.** A skill that turns a tweet, a video, a YouTube video or a landing page into a vertical reel that says what the source says and looks like it, cut to a voice. Its provenance is Meng To's launch reel for HTML Demo (fil.design). It is not bundled here; use it when the user has it installed, under its author's terms.

**The method (reverse-engineered).**
- Read the source: its words word for word, its media, its measured fonts and colours, into `Source.md` and `Look.md`.
- Pick a structure (promo, showcase, "found this", explainer, before and after) and a layout per beat; the creator's face grows as the ask grows.
- A camera placeholder (a backlit studio silhouette) stands where the creator's take will go, so the reel is complete before anyone records.
- Script in the creator's voice from the source's own facts, sized to the voice's pace; voice with word timestamps; every word named (`T.zoom`, `T.htmlEnd`).
- Every HTML scene is drawn from one clock (`window.__frame(t)`) on a 540 × 960 stage rendered at 2×. When the real take arrives, word anchors give a piecewise-linear map from real seconds τ to scratch seconds t, and each scene renders again at t = W(τ): the same animation on the new delivery, without re-animating.
- Assembly in Fil's video editor over MCP, previewed locally first.

**Use it for.** Route A reels from a source, and route D reels where the takes come later.

**What Edit Anything borrows as method.** Word anchors and retiming (`references/edit-craft.md`), the camera placeholder, cover-first hooks, naming every word time.
