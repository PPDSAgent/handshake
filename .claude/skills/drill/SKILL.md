---
name: drill
description: Run a spaced-repetition review of due cards from the deck, plus receptive fingerspelling practice at asl.ms. Use when the learner says "drill", "review", "practice", or when due cards should be cleared before a lesson.
---

# /drill — spaced-repetition review

Follow `rules/tutor-rules.md`. The algorithm is in `learners/README.md` — if the
learner has modified it, their version governs (Rule 7).

## Procedure

1. **Select.** From `learners/<learner>/deck.tsv`: rows with `due ≤ today`, oldest `due` first,
   max 15. Zero due? Say so, offer the asl.ms block (step 3) or `/lesson`, done.
2. **Quiz, one card at a time.**
   - Show `prompt` only. They attempt it (signing or spelling physically —
     remind them this is a hands-on session, not a chat quiz).
   - Then reveal `source_url`; they self-check against the video and self-grade:
     **miss / got it / easy**. Trust their grade — self-assessment against the source
     is the design, because you cannot see their hands (until the Phase 3 webcam lab).
   - Show `answer_hint` after grading, as reinforcement.
   - Apply the algorithm to `ease`, `interval_days`, `due`, `reps`, `lapses`.
   - Misses: brief, factual ("back tomorrow — M and N need one more day"). Two
     misses in a row on the same card → park it and move on; flag it in the journal.
3. **Receptive block (units 1+, ~3 min).** Send them to https://asl.ms/ at the speed
   in `state.md` (`asl_ms_speed`). ≥80% over ~10 words → nudge the speed up one
   notch next time and record the new number. It's their favorite scoreboard; treat it
   that way.
4. **Close.** Rewrite the updated rows to `deck.tsv` (all columns, tabs intact —
   run `python3 tools/verify.py --deck` after writing to prove the file is still
   well-formed). Journal entry (`did`: cards seen, misses by name; `next`; `note`),
   update streak + `last_session` in `state.md`, offer the commit.

## Tone

Fast, rhythmic, low ceremony — a good gym set, not a lecture. Scores plainly stated,
progress numbers surfaced when they move ("interval on HELLO just went to 8 days —
that card is nearly retired").
