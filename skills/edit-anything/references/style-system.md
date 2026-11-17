# The style system (Look.md)

Every project gets one `Look.md` (template in `templates/look.md`). Everything drawn, typed and heard follows it. It is written once, confirmed with one rendered style frame, then reused for the next video so the second one takes minutes.

## 1. Palette

- Five to seven colours with HEX codes and a role each: ground (background), ink (main text and shapes), accent (the one thing to look at), support (secondary shapes), highlight (rare, small).
- One accent per frame. The accent marks what matters now.
- Check contrast for text: at least 4.5:1 for small text, 3:1 for large titles (WCAG). Measure it; do not estimate.
- From an existing brand: take its palette as is. From references: take the temperature and the contrast, not the exact colours.

## 2. Typography

Three roles, never more than two families:

| Role | Job | Typical choice |
|------|-----|----------------|
| Setup | the line that frames | the text face, medium weight |
| Payoff | the word that lands | the display face or the text face at heavy weight, large |
| Labels | captions, numbers, small notes | the text face or a mono, small, tracked |

Rules:
- Choose type by mood axis "type voice", era and audience, not by habit. A quiet serif with air says something different from a heavy grotesk filling the frame.
- If the typeset skill (pbakaus/impeccable) or typography-expert (curiositech/some_claude_skills) is installed, use it to build the scale, the pairing and the micro-typography. Otherwise use a modular scale (1.25 for calm, 1.5 for loud) from the caption size up.
- **Licences:** use only fonts the user owns or that are free for video (Google Fonts are under the SIL Open Font License or Apache and may be used in video). Never embed a font you cannot license. Note each font and its licence in `Look.md`.
- On screen: captions at least 4% of the frame height on 9:16; no more than two lines; no text in the platform's unsafe areas (`references/routes.md`).
- Kinetic type: one word or phrase moves at a time, on the word it is spoken; the rest holds still.

## 3. Image language

- What is drawn (illustration, 3D, photo, pixel, diagram) and how (flat, textured, paper, grain).
- How people appear: on camera, as a silhouette placeholder, illustrated, or not at all. Never a generated likeness of a real person without their consent.
- Do's and don'ts in plain words (for example "no stock-photo handshakes", "no cold blue AI glow").

## 4. Motion

- Easing: one family for the whole film (for example ease-out for arrivals, ease-in-out for moves).
- Timing: arrivals 8 to 14 frames at 30 fps; holds long enough to read the text twice.
- Transitions: one or two kinds, used for a reason (a cut for a new idea, a match move for a continuation).
- Camera: still, or one kind of move per scene.

## 5. Sound palette

- The voice: whose voice, what pace, close or roomy.
- Music: mood, tempo range, licence (owned, royalty-free with licence, or made for this film).
- Effects: one family (soft UI pops, wood knocks, paper and pen, digital glitches) that matches the texture axis. Earshot's bank and Explainer Studio's kit both offer families made in code, so there is nothing to license.

## 6. Do's and don'ts

Five to ten short lines the user agrees with. They become the first entries in `checks.md`.

## Confirm with a style frame

Render one frame (or a three-second loop) of the hook in the new look and show it before building the rest. Changing the look now costs a minute; after the build it costs the build.
