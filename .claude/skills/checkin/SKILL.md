---
name: checkin
description: Run the weekly review — recap the week's wins from the journal, check the current unit's partner mission and book it if unstarted, and pull in any new Handshake Lite relay lines. Use when the learner says "checkin", "check in", "weekly review", "how'd this week go", "let's do our weekly", or when seven-plus days have passed since the last checkin journal entry.
---

# /checkin — weekly review, partner mission, relay

Follow `rules/tutor-rules.md` throughout, **including Rule 1**. This skill does not
*teach* signs, but it routinely handles sign glosses: the relay line's `nemeses` field
names the partner's problem signs (e.g. `nemeses: WATER, PLEASE, SORRY`), and
`learners/shared/missions.md` rows are full of glosses too (unit 05: "EAT, DRINK,
SLEEP, HOME, HELP, WANT"). Reading a gloss name aloud is not a Rule 1 violation — it's
just the word, not a description of how to produce it. The violation happens if a
learner responds to hearing a nemesis or mission gloss with "just tell me how to make
WATER" and the tutor answers from memory instead of pointing at that card's
`source_url` or the lookup flow. Stay alert for that moment in every part below.

Rule 4 (log or it didn't happen) and Rule 7 (the learner's version governs) also
apply to what this skill writes. Relay data about a partner is treated the same way a
partner's journal is (CLAUDE.md, `learners/README.md` §pairing model): streaks and
unit position are shared within a pair, nothing is shared outside it — see the pair
scoping in step 3.

Three parts, all required, in this order: weekly review, partner mission, relay.

## Procedure

### 1. Weekly review

- Read the last 7 days of `learners/<learner>/journal.md` and current `state.md`.
- Pull **wins**, concrete and quoted from the real `did:` lines — not paraphrased,
  not invented. If a week has no entries, say that plainly; there is no win to
  manufacture.
- State streak health as a fact, no guilt either direction ("streak: 4, one day
  missed Tuesday" is complete — don't editorialize on the miss, per Rule 5).
- Name **one** focus for next week, drawn from the most recent `next:` line or a
  pattern across the week's misses (e.g. a card lapsing twice). One focus, not a list.
- **From unit 11 onward** (check `current_unit` in `state.md`): nudge toward a local
  Deaf community event. Use the National Association of the Deaf link from
  `curriculum/sources.md` (`https://www.nad.org/`) — do not invent a specific local
  event or organization; point them at NAD's own resources to find one.

### 2. Partner mission

- Read `learners/shared/missions.md`. Find the row for the learner's `current_unit`
  (from `state.md`), zero-padded to match the table's two-digit unit column — e.g.
  `current_unit: 4` in `state.md` is row `04` in the table.
- **Partner-not-live guard first:** if `profile.md` has `partner: none`, or the named
  partner has no directory under `learners/`, or that partner's surface isn't built
  yet (the app itself doesn't exist yet for them to use — check whether Handshake
  Lite is marked shipped in `docs/`, not a profile field; there's no per-learner flag
  for this) — do not discuss the mission or ask how partner practice is going. Offer
  the current unit's solo `## Family mission` from `curriculum/` instead, and stop
  here.
- Otherwise, report the mission row's status by what's actually in the **Log**
  section, not the Status cell alone — the Log is the record of what happened:
  - **Completed** (a dated Log line for this unit already exists, and the Status
    cell reads `completed`): read the Log line back, don't re-ask.
  - **Not started, nothing scheduled yet** (Status cell is `not started`, no Log
    line for this unit at all): this is the one case where `/checkin` books
    something concrete. Ask for a real day and time this week ("when can you two do
    this?"). Once they give one, **append a Log line** — do not leave it as an
    abstract "sometime this week," and do not touch the Status cell: it stays
    `not started` until the mission is actually done, because that's the exact
    value `/report` checks (`/report` SKILL.md step 7) to keep recommending it. A
    Log line reading anything but a real, completed mission must never contain the
    word `completed`.
  - **Scheduled but not yet confirmed done** (a Log line says `scheduled: ...` for
    this unit, Status cell still `not started`): ask if they did it. If yes, treat
    it as the completed case below. If not yet, leave everything as-is — no new
    write, and don't press.
  - **Reported complete just now** (whether or not it was scheduled first): ask one
    sentence on how it actually went, then append a dated Log line — `<date> — unit
    <NN>: <one sentence>` — **and** change that row's Status cell from `not started`
    to `completed`. Both writes happen together; a completed mission with no Status
    flip would leave `/report` recommending a mission that's already done.
  - Sign glosses appear in the mission text itself — Rule 1 applies here exactly as
    in the header note above: read them, never describe how to produce them.

### 3. Relay

- Read the current learner's `partner` field in `profile.md` **first**. If it's
  `none`, there is nothing to relay for this learner — say so and skip the rest of
  this section entirely.
- Read `learners/shared/relay.md`. The line format is specified in
  `learners/README.md` §Relay — reference it there when parsing, don't restate the
  field list here as a second copy; the producer (Handshake Lite) and this consumer
  must never drift out of sync.
- **Pair scoping (privacy-critical):** `relay.md` is a shared file and may carry
  lines from people who are not this learner's partner. Derive a slug from each
  line's exported name the same way as first-sighting below (lowercase, spaces to
  hyphens) and **only act on the line whose derived slug matches this learner's
  `partner` field.** Any other name in the file is a different pair's data — do not
  parse it, do not create a directory for it, do not mention it in this session or
  write it to this learner's journal. This mirrors `/report`'s partner-only
  disclosure and `learners/README.md`'s "partners see each other's streaks" scope;
  outside a pair, none of this is shared.
- Of the matching partner's lines, take only the **newest** one.
- **Staleness check before anything else — including before creating a directory:**
  compare that line's trailing date to today. If it is **older than 14 days**,
  report the partner's status as **UNKNOWN** and stop here for this section: do not
  create a directory from it, do not parse it, do not update any `state.md`. A gap
  is a gap, not a verdict — never say or imply they stopped practicing.
- **New name, first sighting** (line is within 14 days and no directory exists yet
  at `learners/<slug>/`): derive `<slug>` from the relay line's display name —
  lowercase it, replace spaces with hyphens (e.g. "Alex" → `alex`) — and confirm it
  equals this learner's `partner` field (it must, by the pair-scoping check above).
  Copy `learners/_template/` to `learners/<slug>/`. In the new `profile.md` set
  `learner: <slug>` (must match the directory name — `tools/verify.py --learners`
  checks this) and `display_name:` to the name as it appeared in the relay line;
  set `surface: lite`. **Leave `tutor_name`, `goal`, `background`, and `partner` at
  the template's placeholder values** (`TUTOR_NAME_PENDING`, `GOAL_PENDING`, etc.) —
  do not invent a tutor name or any other field by find-and-replace. Those fields
  belong to that person's own onboarding (Handshake Lite's, not this session's); a
  fabricated value is worse than a visible placeholder, and nothing here ever runs
  a Boot Ceremony on their behalf — that only triggers for *this machine's* learner
  in `learners/current.txt`. In `state.md`, add `last_relay: never` per
  `learners/README.md` §Per-learner files. Leave `journal.md` exactly as copied
  (still carrying the template's EXAMPLE entry) — don't write to it from a relay
  line; it clears itself the first time that learner has a real session logged.
- **If the line is newer than that learner's recorded `last_relay`** (treat the
  literal string `never` as older than any real date — any relay line is newer than
  `never`): parse it field by field exactly as `learners/README.md` §Relay specifies
  (read the spec fresh; don't rely on a paraphrase). Update `current_unit`,
  `streak`, `asl_ms_speed`, and `last_relay` in that learner's `state.md` from the
  parsed values — **and only those four fields.** Do not write `last_session`: the
  relay line's date is when they exported, not necessarily when they last
  practiced, and `last_session` is not part of this skill's write set.
  - **Hard rule — no inferring:** if any field doesn't parse cleanly (missing
    separator, non-numeric where a number is expected, malformed date), do **not**
    guess a value. Leave that field alone in `state.md` and report by name exactly
    which field(s) failed to parse, quoting the raw line. A malformed line means
    "ask the learner to re-export," not "guess and move on."
  - The `nemeses` field names sign glosses — Rule 1 applies (see header note):
    report the names, never describe how to produce them.
- If the line is not newer than `last_relay`, nothing to do — say so briefly.

### 4. Close

- Write the weekly journal entry to `learners/<learner>/journal.md`:
  `## <date> — weekly checkin` as the heading, then `did` / `next` / `note` lines
  covering all three parts above (what the review surfaced, mission status/booking,
  relay result for the partner only — never another pair's data, per step 3). This
  heading intentionally differs from the per-session `## <date> — session N (unit U,
  streak S)` shape in `learners/README.md` — a checkin isn't a numbered practice
  session. `/report`'s asl.ms-speed scan matches on the text `asl.ms ... speed <n>`
  inside an entry, not on the heading, so both heading shapes coexist without
  confusing it.
- Update `state.md`:
  - For the checked-in learner themself: **nothing.** A checkin is a review of
    history, not a practice session — it does not bump `streak` or `last_session`.
    Those only change in `/drill` and `/lesson`.
  - For the relaying partner, only if step 3 parsed a newer line: `current_unit`,
    `streak`, `asl_ms_speed`, `last_relay` — the same four fields and no others.
- Offer `git commit`.

## Tone

Same colleague register as the rest of the tutor — no cheerleading, no guilt. This is
a Monday-morning standup, not a performance review: state what happened, name one
thing to do next, move on.
