# Outside judges

You never grade your own render. Something other than you or the user decides whether it worked: a measurement, a listening tool, blind judges, and later the real numbers.

## 1. The measured check (always)

`python3 scripts/verify_export.py film.mp4 --target social [--transcript words.json --captions film.srt] [--expect-seconds 30]`

| Check | Pass when |
|-------|-----------|
| Video stream | present, the expected resolution and shape |
| Audio stream | present |
| Length | within ±0.5 s of the board's length, or of `--expect-seconds` |
| Integrated loudness | within ±1 LU of the target (-14 LUFS for social, -23 for broadcast) |
| True peak | at or below -1 dBTP |
| Black frames | no black stretch longer than 0.3 s except a planned fade |
| Frozen picture | no unplanned freeze longer than 2 s |
| Captions | at least 98% of the transcript's words appear in the captions in order (when both are given) |

The script prints a plain pass or fail list and exits 1 on any fail. Report the numbers, not just "passed".

## 2. The listening check (when earshot is installed)

`earshot timeline` for sync of effects to cuts, `earshot critique` for the mix scorecard. See `references/sound.md`.

## 3. Blind judges (for a draft that matters)

Give two subagents only the brief (goal, viewer, platform) and two renders labelled A and B in random order (for example the first draft and the revised one). Each says which does the job better for that viewer and why, in three lines. If both prefer the newer one, ship it; if they split or prefer the older one, read their reasons and fix before shipping. Never tell the judges which one is newer.

## 4. The user's eyes

Show the contact sheet and the render. The user's "this is not me" outranks every number.

## 5. The real numbers (after publishing)

Retention at 3 seconds, average view duration, completion, and the action from the goal (clicks, replies, sign-ups). Read them from the platform's insights (Edits and Instagram show them per reel) and write what they say into `checks.md` (`references/learning.md`).

## Hard targets

Treat these as reasonable: every measured check passes on the first full render; captions at least 98% correct; the hook understandable with the sound off. A missed target with honest numbers is a good result. A faked pass is not.
