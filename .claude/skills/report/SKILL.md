---
name: report
description: Show a progress dashboard — streak, unit position, deck stats, asl.ms speed trend, and a misses leaderboard, plus the partner's status if paired. Read-only, never touches any file. Use when the learner says "report", "progress", "how am I doing", "show my stats", "dashboard", "where do I stand", "what are my numbers", "how's the deck looking", "am I due for review", or "how's my partner doing".
---

# /report — progress dashboard

Follow `rules/tutor-rules.md` throughout, especially Rule 1: this skill never
describes how to produce a sign from model memory — no handshape, movement,
location, or palm-orientation description, no "it looks like…" from recall.
`/report` only ever points at a `source_url` or hands off to `/coach`; it does not
teach. This skill is also read-only in a second sense: it **never writes to any
file** — no `state.md`, no `journal.md`, no `deck.tsv`. Say so in the report itself
("nothing on disk changed").

On Rule 4 (log or it didn't happen): a report by itself isn't a session, so it
doesn't generate its own journal entry — there's nothing that happened here beyond
reading files. That's a description of what this skill does, not a carve-out from
the rule: if `/report` runs inside a `/lesson`, `/drill`, or `/coach` session, that
session's own journal entry (written by that skill, per Rule 4) still covers
everything that happened. `/report` never substitutes for it and never skips it.

Every number below is **computed** from the files at report time, not estimated or
recalled from earlier in the conversation. If the learner asks "how did you get that,"
show the arithmetic — the steps below are written so you can restate them directly.

## Procedure

1. **Load context, read-only.** Read `learners/current.txt` for the slug. If the
   file is missing, there's no learner directory on this machine yet — say so and
   hand off to the Boot Ceremony (`curriculum/unit-00-boot-ceremony.md`) per
   CLAUDE.md's session-start protocol instead of running a report on nothing.
   Otherwise read `learners/<learner>/profile.md`, `state.md`, `journal.md`, and
   `deck.tsv`. Do not open these with any intent to edit — this skill has no write
   step, anywhere.

2. **Core stats — straight from `state.md`.**
   - Streak: the `streak` value, as-is.
   - Unit position: the `current_unit` value, as-is.
   - Last session: the `last_session` value — compute the gap to today; flag it if
     it's more than 2 days ("last session Aug 10, 3 days back") rather than staying
     silent on gaps. 2 days or fewer: state the date without comment.

3. **Deck stats — counted from `deck.tsv`.** Parse every row after the header. Today
   is the date this report runs.
   - **Total** = row count.
   - **Due today** = rows where `due <= today`. Label it that way, not just "due
     today" — this bucket folds in any overdue backlog along with cards due exactly
     today (same selection rule `/drill` uses), so say "N due (due ≤ today)" rather
     than implying every one of them became due this morning.
   - **Retired** = rows where `interval_days >= 21`.
   State the counts *and* which ids landed in each bucket if the learner pushes on it
   — e.g. "4 due: u1-fs-a, u1-fs-b, u1-fs-m, u2-water."

4. **asl.ms speed trend — pulled from journal history, never guessed.** Scan
   `journal.md` entries for `asl.ms ... speed <n>` mentions, oldest to newest. This
   depends on `/drill` having narrated the speed in its `did:` line, which is
   customary but not a required field — `learners/README.md`'s journal spec only
   fixes `did` / `next` / `note` as free text, so a real learner's journal can
   legitimately have zero matches even after plenty of drilling.
   - **Two or more matches:** report the sequence you actually found (e.g. "3 → 4 →
     4 → 5 over the last four sessions") and confirm it matches the current
     `asl_ms_speed` in `state.md` — if it doesn't, say so plainly rather than
     papering over the mismatch.
   - **Fewer than two matches, and `state.md`'s `asl_ms_speed` is the template
     default (`not yet measured`)** — say plainly there's no speed history yet;
     nothing to trend, nothing to cross-check.
   - **Fewer than two matches, but `state.md` shows a real number** — don't say "not
     enough history yet" (that reads as "no drilling happened," which may be false).
     Say instead: "state.md shows speed `<n>`, but the journal doesn't have enough
     `asl.ms ... speed` mentions to show a trend" — the current value is real, the
     trend line just isn't reconstructable from what's on disk.

5. **Nemeses leaderboard — ranked by the `lapses` column.** Sort all deck rows by
   `lapses` descending, keep the nonzero ones, show the top 3–5 with their `id` and
   `lapses` count. Ties stay tied (list both). Zero cards with lapses: say the deck
   has no repeat misses yet — that's a real result, not a gap to fill.
   - If discussing *why* a card is a nemesis, stay inside Rule 1 in full: point at
     the `source_url`, ask what they saw, never describe the handshape, movement,
     location, or palm orientation yourself, and never hedge with "I think it's
     roughly a flat hand near the chin" — a hedge is still a violation.
   - If the learner pushes past that ("just tell me how to make WATER, don't send
     me another video"), don't soften into a description. Say plainly that this
     skill doesn't do sign production — same law everywhere in this system — and
     hand off: "that's a `/coach` question, not a `/report` one — want me to switch
     to it?" If you notice yourself starting to describe a sign from memory
     mid-sentence, stop, say so out loud, and redirect to the link — the same
     self-catch protocol `/coach` uses.

6. **Partner section — only if `profile.md`'s `partner` field isn't `none`.**
   - **No directory at `learners/<partner>/`** → say the partner's system isn't set
     up yet. Do not invent a streak, a unit, or a reason. Treat the partner as
     **not live** for step 7.
   - **Directory exists, partner's `profile.md` surface is `claude-code`** → read
     their `state.md` directly and show streak + unit position beside the learner's.
     This is live state. Treat the partner as **live** for step 7.
   - **Directory exists, surface is `lite`** → `learners/README.md` currently
     documents `lite` as still in build, so treat the partner as **not live** for
     step 7 (the partner-mission recommendation) even though there's real data to
     show here. Their `state.md` is a relay snapshot, not live state:
     - If `last_relay` is literally `never` — the template default `/checkin`
       writes on first sighting (`learners/_template/state.md`,
       `.claude/skills/checkin/SKILL.md`) — there's no relay history yet. Report
       their status as **UNKNOWN — no relay received yet**. Don't do date
       arithmetic against `never`.
     - Otherwise, compare `last_relay` to today. More than 14 days back → report
       status as **UNKNOWN** — do not show the stale streak as current, and do not
       say they "stopped" (a quiet phone is not a quiet learner). Within 14 days →
       show the streak/unit but label it "relayed as of `<last_relay>`," not
       "current."
     - **Also check `learners/shared/relay.md`** if it exists, for this partner's
       newest line (format is in `learners/README.md` §Relay — reference it there,
       don't restate or parse it here; `/checkin` is the one parser, so the spec
       has one home). If that line's trailing date is newer than the `last_relay`
       you just read, there's an unprocessed relay sitting in the file: say so by
       name — "there's a relay line dated `<date>` that hasn't been pulled in yet —
       run `/checkin` to update their numbers." Keep showing the numbers already in
       `state.md` (labelled as of `last_relay`); `/report` never parses relay
       fields itself or infers values from an unprocessed line — that's
       `/checkin`'s job, and duplicating it here is how the two drift apart. If
       `learners/shared/relay.md` doesn't exist yet, or has no line newer than
       `last_relay`, say nothing extra here.
   - Never read the partner's `journal.md`. Streaks and unit position are shared;
     what someone wrote about struggling is not (CLAUDE.md: "Never read one
     learner's journal aloud to another"; `learners/README.md` §pairing model says
     the same).

7. **Exactly one recommendation, computed in this order — first match wins:**
   1. Due today > 0 → `/drill` (reviews before new material, `rules/tutor-rules.md`
      Rule 5).
   2. Due today == 0, **and step 6 classified the partner as live** (directory
      exists, surface is `claude-code`) — a `lite` partner or a missing directory
      does not qualify, same Partner-not-live guard `/checkin` applies — and
      `learners/shared/missions.md` exists and the current unit's row in it is
      still `not started` → do that partner mission. If `missions.md` doesn't
      exist yet, there's no catalogue to check — fall through to branch 3.
   3. Otherwise → `/lesson`, continue the current unit. This is also where a
      not-live partner lands: solo material, not a partner-mission ask, per the
      guard above.
   State which branch fired and why, in one line — the learner should be able to
   check your logic against the same files.

8. **Render the report** — the numbers above, the partner block if applicable, the
   one recommendation, and a closing line that nothing on disk changed.

## Tone

An engineer's dashboard, not a pep talk. Lead with numbers. Narrate movement only
where the files actually let you compute a before-and-after: the asl.ms speed
sequence from step 4 ("speed 3 → 4 → 4 → 5"), and misses a journal entry explicitly
names for this or a recent session. Don't narrate an `interval_days` delta — a
single `deck.tsv` snapshot carries no prior value to diff against, so "interval on
HELLO just went to 24 days" isn't something this skill can compute (that line
belongs to `/drill`, which does the review in the same session it happens). State
the current value plainly instead: "HELLO: interval 24 days — retired." No
cheerleading, no guilt about gaps — state the gap as a fact (`rules/tutor-rules.md`
Rule 5) and move to the recommendation.
