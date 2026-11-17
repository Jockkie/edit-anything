# Sound

Sound first: the voice and the music decide the cuts. You cannot hear, so you measure and you listen with earshot (`references/engines/earshot.md`). Never say how something sounds without a reading or a number.

## The voice

- **Whose voice.** The user's own recording first. A cloned voice only with the speaker's explicit consent, and never the voice of someone else. A synthetic stock voice is fine when the user chooses it.
- **Clean-up order:** remove hum and noise gently, cut breaths that are too loud (keep the natural ones), level the phrases, then a light compressor so quiet words stay audible.
- **Pace:** tighten long pauses (`references/edit-craft.md`), never speed up the voice so it sounds rushed.

## Music

- Licensed, royalty-free with a licence the user keeps, or made for this film. Never a commercial track without a licence; platforms mute or block it.
- Choose by the mood axes (energy, temperature, pace). With earshot installed, `earshot rank "<description>" music/` shortlists candidates.
- Beat grid: `scripts/beats.py music.wav` gives tempo and beat times for cutting.
- Under a voice, the music sits low and ducks under speech (sidechain or volume automation), then rises in the gaps.

## Effects

- One family that matches the texture axis of `Look.md`: soft UI pops, wood knocks, paper and pen, digital glitches, whooshes.
- Made in code, so nothing to license: earshot's bank (252 sounds, `earshot sfx`, `earshot kit` with measured onset and peak) or Explainer Studio's kit (pen, chalk, brush strokes, paper, pops, whooshes, impacts).
- Place each effect against its cut: a tap leads the cut slightly, a whoosh peaks just after it, an impact lands on the frame. With earshot, `kit` reports where each one sits.
- Fewer is better: an effect on every cut becomes noise. Effects sit under the voice, not on top of it.

## Loudness targets (measure, do not guess)

| Delivery | Integrated loudness | True peak |
|----------|---------------------|-----------|
| Social and streaming (Reels, TikTok, Shorts, YouTube) | about -14 LUFS (±1) | at or below -1 dBTP |
| Broadcast in Europe (EBU R128) | -23 LUFS (±0.5) | at or below -1 dBTP |
| Podcast-style talk | about -16 LUFS | at or below -1 dBTP |

These are common working targets, not platform rules; platforms normalise loudness themselves. Measure with `scripts/verify_export.py` (ffmpeg's ebur128) or `earshot measure`. Normalise with ffmpeg's `loudnorm` in two passes when the measurement is off.

## The listening check

Before delivery, with earshot installed:
1. `earshot timeline film.mp4 --video film.mp4`: the events, the loudness over time, and whether effects land on the picture cuts.
2. `earshot critique film.mp4`: a scorecard with timestamped fixes. Fix the major ones first.
3. Report the numbers to the user, for example "integrated -14.2 LUFS, true peak -1.4 dBTP, 21 of 23 critique metrics in range".
