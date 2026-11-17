# Self-check (visible to the user)

Run this before Gate 1, Gate 2 and every delivery, and show the result as a short block titled "Self-check". If an item fails, fix it first and say what you fixed. Never claim a check passed that you did not run; write "runs after your answer" instead.

## Checklist
1. **Sources:** `seen` only for what the user said or showed, with their words as `quote`. Footage or pages you have not seen are `unknown`. With code: `python3 scripts/check_dossier.py edit.json --gate <1|2|deliver>` passes.
2. **No invented facts in the script:** every claim in the board is in the claim register with its proof; numbers come from the user or a source you read.
3. **Measured, not guessed:** every number about a render (loudness, length, caption accuracy, sync) comes from `scripts/verify_export.py` or earshot, with the tool named.
4. **One question:** your message ends with exactly one question.
5. **Gate confirmed:** the user confirmed the brief (Gate 1) or the whole board (Gate 2) themselves.
6. **Rights:** music, fonts, footage and engines are licensed for this use; no one's face or voice without consent; credits listed.
7. **Money:** affiliate disclosure before any link; a quote and a cap before any paid call; the actual cost reported after.
8. **checks.md:** every line in it was checked against the contact sheet before rendering.
9. **Files:** you name only files that exist; the handoff matches the editor the user chose.

## Assumptions block (in every gate summary and delivery)
Show "What you told me and what I assumed": what the user said (with quotes), what you estimated (with its basis), and what is still unknown. With code: `python3 scripts/check_dossier.py edit.json --assumptions`.
