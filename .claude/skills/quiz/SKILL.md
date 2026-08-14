---
name: quiz
description: Run a unit's Checkpoint as a live check to decide whether the learner advances to the next unit. Use when the learner says "quiz", "checkpoint", "test me", "am I ready for the next unit", "did I pass", or when it looks like this unit's checkpoint boxes are all satisfied and it's time to confirm before advancing.
---

# /quiz — checkpoint runner

Follow `rules/tutor-rules.md` throughout. Especially Rule 1: nothing here describes
how to produce a sign from memory — every checkpoint item is a link, a timed task, a
read against stored history, or a live read by a real person, never a recall prompt
answered from the tutor's memory.

**The honest limit, stated up front (same one `/drill` states):** the tutor has no
camera and no access to the learner's screen or hands — that's still true here, and
this skill does not pretend otherwise. "Checkpoint" does not mean the tutor *observes*
the sign. It means each item is graded against something outside the tutor's own
opinion — a clock the tutor actually runs, a score an external site displays, drill
history actually stored in `deck.tsv`/`journal.md`, or a real person other than the
tutor reading the learner back — instead of "yeah, I can do that." That is a
real, if narrower, bar than a bare self-report, and it is the same bar `/drill` uses
for its receptive block. Don't oversell it as more than that.

**This skill defers to `/lesson`'s Unit-complete protocol.** They implement the same
rule and must not disagree: the pass/fail decision is binary — all-pass or any-fail,
exactly like `/lesson` — congratulate once, bump `current_unit`, preview the next
unit's *Why* in a sentence; any fail → that item becomes tomorrow's journal `next:`
line, no shame. An item that couldn't be run at all this session ("not-yet-measured")
is *not* a third outcome — for the advance decision it counts as a fail, same as a
missed threshold. The two words exist only so the journal's `next:` line can say
accurately "wasn't able to attempt this yet" versus "attempted and missed," which
matters for what tomorrow's plan looks like. If you ever edit the advance/fail logic
in one skill, make the matching edit in the other or the two commands drift apart.

## Procedure

1. **Load context.** `learners/<learner>/state.md` (`current_unit`, `asl_ms_speed`),
   that unit's `## Checkpoint` section from `curriculum/unit-<NN>-*.md`, this unit's
   rows in `learners/<learner>/deck.tsv`, and the last several `journal.md` entries —
   several of the item types below are graded from what's already stored there, not
   from running something live.

2. **Precondition check.** `current_unit` only ever advances when this skill (or
   `/lesson`'s mirrored logic) records an all-pass — so `current_unit` itself is the
   only per-unit pass signal the system keeps. If the unit being asked about is
   *behind* `current_unit`, its checkpoint already passed by construction; ask why
   they want to re-run it (refresher? confusion about where they are?) rather than
   assuming. If it's the current unit, this is the normal call — proceed. **Never
   tick, edit, or otherwise touch the `- [ ]` boxes in `curriculum/unit-<NN>-*.md` —
   that file is shared across every learner.** Results live only in *this* learner's
   `journal.md` and `state.md`.

3. **Say what this is.** One line, honestly framed per the note above: this checks
   each item against a clock, an external score, stored history, or a real person —
   not a chat about whether they feel ready.

4. **Time budget.** Same 15–20 minute cap as any other session (Rule 5). Some
   checkpoints — a timed production item, an asl.ms block, and a live family call in
   the same unit — can genuinely eat the whole window on their own. Run what fits
   cleanly; anything that doesn't becomes a "checkpoint continues" `next:` line for
   tomorrow. Never rush a real person on a call, and never fudge a timing threshold
   just to close the checkpoint out in one sitting.

5. **Run each checkpoint item.** Match the item's own wording to one of these — the
   *how* comes from what the item says, never from tutor memory of the sign:

   - **Timed/live production** ("Produce A–Z from memory... under 60 seconds,"
     "Produce all 12 signs... twice without a miss," "Sign 'ME LOVE FAMILY' as one
     smooth sequence"): the tutor runs a real clock and watches the wall-clock time,
     which it *can* measure objectively. Correctness the tutor cannot judge — it has
     no camera — so immediately after the attempt, reveal the item's source
     link(s)/deck cards and have them self-check against the video, exactly the way
     `/drill` does after every card. Pass = met the stated threshold (time, no
     source open, no miss) *and* their honest self-check against the source cleared.
     This also covers items phrased around another person's judgment, like
     "smoothly enough that a stranger could read it" — the tutor is not that
     stranger and does not stand in for one; grade it via self-check-against-source,
     or route it into the next category if the item specifically calls for a human
     reader.
   - **External-instrument item** (asl.ms reading blocks): send them to
     https://asl.ms/ now, run the real block at the stated speed. If the site
     displays a score, read it off; if it doesn't, tally hits/misses manually the
     same way `/drill`'s receptive block does. Record the number immediately, as it
     happens — not from memory of a past run.
   - **Deck/history item** ("two consecutive `/drill` sessions clear this unit's
     cards at ≥80%," "most recent `/drill` pass logged with zero misses"): this is a
     read, not a live re-run. Check this unit's rows in `deck.tsv` (`reps`,
     `lapses`) against the last few `journal.md` `did:` lines and answer from what's
     actually recorded. If the history isn't there yet, that's not-yet-measured —
     don't ask the learner to re-drill on the spot to manufacture it; that's
     `/drill`'s job on its own schedule.
   - **Event / witnessed-by-a-real-person item** ("Used AGAIN mid-conversation to
     genuinely request a repeat," "Read a family member's name signed to you on a
     video call," "Hold a 5-minute conversation with a partner," "Actually use
     PLEASE-SIGN-SLOWLY because you were genuinely lost"): this either happens live,
     right now, with an actual other person (on a call or in person) — or it must
     already be logged with dated, specific evidence in a prior journal `did:` line
     (not "yeah, I do that"). Neither available this session → not-yet-measured, no
     argument, no accepting the claim as a substitute.
   - **Meta-knowledge item** ("Explain the double-letter technique in one
     sentence"): answered in conversation, but graded as a comprehension check of
     what they saw on the source video — not the tutor supplying or confirming the
     technique from its own memory. Vague or wrong → fail; point back at the source
     link, don't fill the gap yourself.

   If the learner pushes back mid-item — "just tell me how, don't send me another
   video" — hold the line the way `/drill` does: the source link *is* the answer
   key, that's what makes this a measurement instead of the tutor guessing. Point at
   it again; don't describe the sign to end the friction.

   After each item, state plainly what was measured — the number, the time, the
   yes/no, the "not-yet-measured, here's why" — never an impression.

6. **Record per-item results as you go.** Keep a running list with the measured
   evidence (score, seconds, observed outcome, or "not-yet-measured: <reason>") for
   each checkpoint line — this is what goes into the journal, not a summary verdict.

7. **Decide, per the Unit-complete protocol (`/lesson`'s, mirrored here) — binary,
   no third branch:**
   - **All pass:** one plain congratulation — no pep talk, no cheerleading. Bump
     `current_unit` in `state.md`. If this unit is 12, there is no next unit — say so
     plainly and note the core curriculum is complete instead of previewing
     anything. Otherwise, load `curriculum/unit-<NN+1>-*.md` and preview its *Why
     this unit* in a single sentence. Do not start teaching it now; that's
     `/lesson`'s job next session.
   - **Any fail** (includes every not-yet-measured item): no shame, no
     re-explaining the sign from memory. State which item(s) didn't clear — missed
     threshold vs. not-yet-attempted — and the measured evidence plainly.
     `current_unit` in `state.md` stays unchanged. The failed/unmeasured item(s)
     become the `next:` line, worded as the concrete next attempt ("re-run asl.ms
     read at speed 3," "checkpoint continues: family video call for the name-read
     item," not "get better at reading").

8. **Close per Rule 4 — log or it didn't happen.**
   - Journal entry (`did`: which items were measured and their results, including
     not-yet-measured ones and why; `next`: the failed/unmeasured item(s) or, on an
     all-pass, the next unit's opening move; `note`: anything worth remembering).
   - Update `state.md`: `last_session` and streak always; `current_unit` only on an
     all-pass; `asl_ms_speed` whenever a reading-speed item was actually run this
     session (unit 01's baseline, unit 12's exit retest, or any refresher run in
     between) — same field `/drill` writes, updated here for the same reason: unit
     12's exit retest is graded against exactly this number.
   - Offer `git commit` — e.g. `git add -A && git commit -m "checkpoint: <date> unit <N> <pass|partial>"`.

## Tone

Plain and factual, like reading off a test result — not a verdict on the learner as
a person. A pass is one sentence, not a celebration. A partial pass is "here's what's
left," not a critique. The checkpoint measures the unit, not them.
