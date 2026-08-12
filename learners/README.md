# Learners — Formats, the Algorithm, and the Pairing Model

Everything here is yours: plain text, greppable, hackable. If you rewire the
algorithm, the tutor follows your version (Rule 7).

## How learners come to exist

The repo ships with no learners — only `_template/`. A learner directory is created
by copying it:

- **Computer-side** (`surface: claude-code`): the Boot Ceremony
  (`curriculum/unit-00-boot-ceremony.md`) copies `_template/` to
  `learners/<your-slug>/` and fills in the profile with you.
- **iPad/phone-side** (`surface: lite`): Handshake Lite keeps its own state on the
  device. The first time one of its export lines is pasted into
  `shared/relay.md`, `/checkin` creates `learners/<slug>/` from the template and
  snapshots the exported values into it.

**Who am I?** `learners/current.txt` holds one line — the learner slug for *this
machine*. It's gitignored, because it's a property of the machine, not the repo.
The Boot Ceremony writes it. If it's missing, the tutor runs the ceremony.

## Two surfaces

| Surface | What it is | How progress gets here |
|---|---|---|
| `claude-code` | The full file-based system on a computer, tutored by Claude Code | Written live, every session |
| `lite` | Handshake Lite — a tap-to-drill web app (in build; see the plan in `docs/`) | **Relayed.** Real progress lives on the device; the files here are periodic snapshots (see Relay below) |

`shared/` holds what belongs to a learning pair rather than either person.

## Per-learner files

**`profile.md`** — set once, rarely changes. Keys: `learner` (slug), `display_name`,
`tutor_name`, `goal`, `surface`, `track`, `partner`, `background`. The field notes in
`_template/profile.md` explain each.

**`state.md`** — changes every session: `current_unit`, `streak`, `last_session`,
`asl_ms_speed` (fingerspelling reading speed — the number that goes up). Lite-surface
learners also carry `last_relay`.

**`journal.md`** — newest entry at top, three lines each:

```
## 2026-08-14 — session 4 (unit 1, streak 4)
- did: drill 12 cards (2 miss: M/N confusion), asl.ms 3 min @ speed 4, taught cluster B C O F D
- next: re-drill M/N first, then cluster L Y I J
- note: double letters clicked after the video
```

The `next` line is what makes tomorrow start fast — the tutor reads it before you
arrive.

**`deck.tsv`** — the spaced-repetition deck, tab-separated, one card per row:

| column | meaning |
|---|---|
| `id` | `u<unit>-<slug>`, unique (e.g. `u1-fs-a`, `u0-hello`) |
| `type` | `fingerspell` \| `vocab` \| `phrase` \| `lookup` (added outside a unit) |
| `prompt` | what the tutor asks (e.g. `Sign: HELLO`) |
| `answer_hint` | context reminder shown *after* the attempt — never a production description |
| `source_url` | the allowlist link that is the answer key |
| `unit` | integer |
| `ease` | float, starts 2.5 (floor 1.3, cap 2.8) |
| `interval_days` | integer, starts 1 |
| `due` | ISO date |
| `reps` | successful reviews, starts 0 |
| `lapses` | misses, starts 0 |
| `added` | ISO date the card entered the deck |

## The algorithm (SM-2-lite)

On each review the learner self-grades against the source video:

- **miss** — couldn't produce it / read it wrong: `interval_days = 1`,
  `ease -= 0.2` (floor 1.3), `lapses += 1`. Due tomorrow.
- **got it** — produced it, maybe hesitantly: `reps += 1`; interval advances
  `1 → 3 → round(interval × ease)`. Due = today + new interval.
- **easy** — instant, no hesitation: as *got it*, plus `ease += 0.1` (cap 2.8).

`/drill` selects at most 15 cards with `due ≤ today` (oldest due first), runs the
session, rewrites the rows. That's the whole engine — about ten lines of arithmetic,
on purpose. Tune it: if reviews feel too easy, raise the starting interval; too
brutal, lower the ease floor. Note experiments in the journal so the data means
something. **Handshake Lite implements the identical algorithm** — this file is the
normative spec for both; if you change one side, change the other or the pair drifts
apart (`tools/test_srs_parity.py`, once built, is the referee).

## The pairing model

Handshake is built for two people learning together. That is a design decision, not
a coincidence: practising with a partner is the strongest retention mechanism
available to an adult learner, and it means neither of you is doing this alone.

- **Shared progress.** Partners see each other's streaks and unit position.
  `/report` shows both. This is encouragement, not surveillance — journals are
  personal, and the tutor never reads one learner's journal aloud to the other.
- **Joint missions.** `shared/missions.md` is the partner-mission catalogue: one per
  unit, designed for two people, with a log of what you've completed. These sit
  *alongside* each unit's own `## Family mission` (which works solo or with anyone).
- **Different tracks, same curriculum.** Same 12 units in the same order;
  track-split units teach each learner the vocabulary of their own world.

## Relay — how a Lite learner's progress reaches this repo

Handshake Lite runs entirely on-device with no account and no network writes. To
share progress the learner taps **Export** and gets one line to text to anyone:

```
Handshake · Alex · day 9 · unit 2 · 34 cards (12 due) · asl.ms speed 4 · nemeses: WATER, PLEASE, SORRY · 2026-08-20
```

Whoever receives it pastes it into `shared/relay.md`; `/checkin` parses the latest
line and updates that learner's `state.md` so `/report` can show the pair side by
side. The app also has a **Backup** button that produces the full deck as JSON, for
real backup or for migrating to the file-based system later.

Deliberately low-tech: it degrades gracefully, needs no account, and anyone can do
it from the couch. If a Lite learner ever wants live sync, the upgrade path is a
paid Claude plan and Claude Code against this same repo — no data migration.
