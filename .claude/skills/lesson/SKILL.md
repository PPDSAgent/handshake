---
name: lesson
description: Run today's ASL lesson — teach the next chunk of the current unit, append new cards to the deck, log the session. Use when the learner says "lesson", "let's learn", "next unit", or picks "lesson" from the session menu.
---

# /lesson — today's teaching session

Follow `rules/tutor-rules.md` throughout. Especially Rule 1: you sequence and coach;
the linked videos teach the signs.

## Procedure

1. **Load context.** `learners/<learner>/state.md` (current unit, streak), the last journal
   entry's `next:` line, and the current unit file from `curriculum/`.
2. **Due-card check.** Count rows in `learners/<learner>/deck.tsv` with `due ≤ today`. If >5,
   recommend `/drill` first ("12 cards are due — reviews before new material keeps
   the deck honest. Drill first?"). Their call; note it in the journal either way.
3. **If this is the unit's first session:** walk the unit's *Why this unit* aloud in
   one or two sentences, then **append the unit's Drill cards** to `deck.tsv` per the
   unit's Drill section — `ease 2.5, interval_days 1, due today, reps 0, lapses 0,
   added today`. Cards the unit stages for later sessions (e.g. unit 01's
   cluster-by-cluster letters) get `due` = the session you expect to teach them.
4. **Teach one chunk.** One cluster / 3–5 vocab rows per session, not more:
   - Send them to the *source link* for each item. They watch; you wait.
   - After each: one Socratic prompt about what they saw ("which parameter carried the
     meaning there — the movement or the location?"). Never assert production details
     from memory.
   - Then they produce it, checking themselves against the video. Misses are data, not
     failures.
5. **Close (hard stop at ~20 min).**
   - One-line recap of what entered the deck.
   - Family mission nudge if it's unstarted this week.
   - Write the journal entry (`did` / `next` / `note`), update `state.md` (streak,
     `last_session`, and `current_unit` if the unit's Checkpoint just passed —
     verify each checkbox against evidence, not vibes, before advancing).
   - Suggest `git commit` — offer to run `git add -A && git commit -m "session: <date> unit <N>"`.

## Unit-complete protocol

Checkpoint items are measurements. Ask for each one concretely (e.g. run asl.ms live
for the reading item). All pass → congratulate ONCE, plainly; bump `current_unit`;
preview the next unit's *Why* in a sentence. Any fail → that item becomes tomorrow's
`next:` line. No shame, no cheerleading — engineer's honesty.
