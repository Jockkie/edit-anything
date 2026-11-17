# The four routes

Every video takes one of four routes. The route decides what you need, what you write, which engines you use and what the user has to do. Pick it from what already exists, not from what sounds nicest.

| Route | When | Length (typical) | The user does | You do |
|-------|------|------------------|---------------|--------|
| **A. Reel** | Vertical, short, from a source (a post, a page, a product, an idea) | 15 to 45 s | Approves the board, optionally records a take | Script, voice, scenes, cut, captions |
| **B. Fully AI-made film** | No camera; the whole picture is made | 30 s to 3 min | Approves board and quotes | Script, voice, scenes in code, generated shots where code cannot, edit |
| **C. Talking head in** | Takes of a person exist | 20 s to 20 min | Shares the takes | Transcribe, paper edit, cut on words, add picture on words, captions |
| **D. Talking head to record** | The person will be on camera | 20 s to 3 min | Records from your shot list | Script in their voice, shot list, then route C |

## Platform defaults (check the live specs before delivery)

| Platform | Shape | Safe area | Length sweet spot | Loudness target |
|----------|-------|-----------|-------------------|-----------------|
| Instagram Reels, TikTok, YouTube Shorts | 9:16, 1080 × 1920 | keep text out of the top 220 px and bottom 380 px | 15 to 45 s | -14 LUFS integrated |
| YouTube (long) | 16:9, 1920 × 1080 or 3840 × 2160 | title-safe 90% | as long as the idea needs | -14 LUFS |
| LinkedIn | 1:1 or 4:5 for the feed, 16:9 for native video | 90% | 30 to 90 s | -14 LUFS |
| Website hero | 16:9 or 21:9, muted autoplay | no captions needed for silent loops | 6 to 20 s loop | not applicable |

These are working defaults, not platform rules. Platform specs change; before delivery check the platform's current guidelines on the web and note the date.

## Route A · Reel

1. Source → facts the reel may say (never more than the source says).
2. Hook in the first 1.5 seconds: the payoff shown first, then the setup.
3. Board, voice (the user's own or a consented cloned voice), scenes on one clock, cut on words.
4. Optional: the user records one take; scenes retime to it (`references/edit-craft.md`, retiming).

Engines: Explainer Studio (styles, reel format), html-reel (when installed; source-based reels with a camera placeholder), motion-graphics boards.

## Route B · Fully AI-made film

1. Story in one sentence, then beats, then shots.
2. Mark each shot: **code** (motion graphics, illustration, 3D, pixel, text) or **generated** (realistic people, places, products in motion).
3. Code shots: Explainer Studio, Lemo-Opuscar styles, Claude Animation Base, three.js, Blender.
4. Generated shots: Flora (Seedance, Kling, Veo and others), always from an approved style frame, never from text alone, with a quote and a cap (`references/tools.md`). Previs a camera move in three.js first when the shot is complex.
5. Voice, music, effects, edit, judges.

## Route C · Talking head in

1. Transcribe word by word (Whisper or the editor's own captions), keep word timestamps.
2. Paper edit on the transcript: mark keep, cut, reorder; remove false starts, filler and repeats; keep the breath before a strong line.
3. Cut on words and breaths, J and L cuts where the voice should lead the picture (`references/edit-craft.md`).
4. Add what is seen on the words that name it: titles, B-roll, animations, a screen recording, a pop-up stat.
5. Captions from the transcript; reframe 16:9 takes to 9:16 by keeping the face in the upper third.

## Route D · Talking head to record

1. Script in the speaker's voice: their own sentences, short, sized to their pace (about 2.6 words a second on camera).
2. A shot list they can follow alone with a phone: framing, light (face to a window), sound (phone close, a quiet room, clothes that do not rustle), two takes per line, a clap or a hand in frame at the start of each take.
3. While they record, build the scenes with a placeholder in the camera position, so the edit is complete before the takes arrive.
4. Then route C on the real takes; retime the scenes to their delivery.
