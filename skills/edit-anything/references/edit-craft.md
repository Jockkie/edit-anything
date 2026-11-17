# Edit craft: how a top editor cuts

Work from the rawest material: the raw takes, the raw audio, a word-level transcript and the beat grid. Never from a summary.

## 1. Transcribe word by word

- Use Whisper with word timestamps (locally: whisper.cpp, MacWhisper, faster-whisper; or the editor's own auto-captions) and keep the JSON with every word's start and end.
- Check names, numbers and brand words against what the speaker meant; correct the transcript, never the audio.

## 2. The paper edit

On the transcript, before touching the timeline:
- Mark **keep**, **cut** and **move** per sentence. Keep the best take of each line; cut false starts, filler ("so, basically"), repeats and the long run-up before the point.
- Find the strongest sentence and consider opening with it (the payoff first, then the setup).
- Read the kept text aloud in order. If it does not make sense read aloud, it will not make sense cut.
- Show the paper edit to the user as the transcript with cuts struck through. This is the cheapest moment to change the story.

## 3. Cut on words and breaths

- Cut in the silence before a word, never inside one. Leave about 2 to 4 frames of air before the first sound of a word.
- Keep the breath before a strong line; cut the breath after it.
- **J-cut:** the next line's audio starts before its picture (the voice pulls the viewer into the next shot). **L-cut:** the picture changes while the previous voice continues. Use them to hide a jump and keep the rhythm.
- Jump cuts on a talking head are fine for social when they remove waiting; cover the ones that jar with a punch-in (scale 110 to 120%) or B-roll.
- Tighten pauses: shorten every pause longer than about 0.6 s to 0.25 to 0.4 s, unless the pause is the point.

## 4. Picture on the words

- Every change of picture lands on the word it belongs to (the "lands on" column of the board).
- Titles appear on their word and stay long enough to read twice.
- B-roll covers a line, not a sentence fragment; start it on a word, end it on a cut.
- Reframing 16:9 to 9:16: keep the eyes in the upper third, follow the face, never cut off the chin and the top of the head at once.

## 5. Cut on the beat (when there is music)

- Get the beat grid with `scripts/beats.py`. Put scene changes on beats where the words allow; the voice wins when they disagree.
- Big moments (reveal, the ask) on a downbeat or a bar start.

## 6. Retiming code scenes to a real voice

Every code scene is drawn from one clock. When a real take replaces a scratch voice:
1. Match named words in both (for example the word that triggers each move) to get anchor pairs (real seconds τ, scratch seconds t).
2. Between anchors, map linearly: t = W(τ). Before the first and after the last anchor, keep the scratch speed.
3. Render each scene again at t = W(τ) for every output frame. The animation follows the new delivery without being re-animated.

## 7. Captions

- From the corrected transcript, two lines at most, cut at phrase boundaries, never mid-name.
- Highlight the payoff word if the look allows; keep everything inside the safe area.
- Export an SRT for the editor and burn in only when the user wants burned-in captions.

## 8. Colour and finish

- One look for the whole film from `Look.md`; match shots to each other before grading them creatively.
- Check skin tones on a talking head; never push them toward green or magenta.
