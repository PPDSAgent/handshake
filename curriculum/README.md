# Curriculum — Unit Format Spec

Twelve units, one markdown file each: `unit-NN-<slug>.md`. Status and sequence live in
`units-index.md`. Units 00–01 are the reference implementations — copy their shape
exactly when building new units.

## Required frontmatter

```yaml
---
unit: 7                     # integer, matches filename
title: Feelings & Health
status: draft               # draft | built | reviewed  (reviewed = maintainer spot-checked)
est_sessions: 4             # 15–20 min sessions to complete
---
```

## Required sections, in order

1. **`## Why this unit`** — 2–4 sentences connecting it to real conversations the learner wants
   to have. Write to a smart adult; no filler.
2. **`## Watch`** — 2–5 links to allowlist lesson pages/videos (`sources.md`), each
   with one line saying what it covers and roughly how long it runs.
3. **`## Learn`** — the vocab table:

   | sign | source | hook |
   |---|---|---|
   | HELLO | https://www.lifeprint.com/asl101/pages-signs/h/hello.htm | your opener for every session — the one you already use in unit 00 |

   - `sign` in small caps (ASL gloss convention).
   - `source` — allowlist URL for **that specific sign**, verified. Lifeprint word pages
     (`pages-signs/<initial>/<word>.htm`) first choice; `signingsavvy.com/search/<word>`
     second; `handspeak.com` entry pages third.
   - `hook` — a short memory aid **about meaning or context**, never a production
     description. Good: "the one you'll use at the audiologist." Bad: "flat hand moves
     from chin" (violates Rule 1 of `rules/tutor-rules.md`).
   - 8–15 signs per unit. Fewer, learned well, beats more.
4. **`## Drill`** — what `/lesson` appends to `learners/<learner>/deck.tsv` when the unit opens:
   normally one `vocab` card per Learn row, plus any unit-specific extras (see unit 01
   for `fingerspell` card examples). State it as a list of card `prompt` values.
5. **`## Family mission`** — one concrete, low-stakes weekly task involving family
   (video call game, teach-one-sign, etc.). Must be doable in under 10 minutes.
6. **`## Checkpoint`** — 3–5 observable pass criteria ("read 5-letter words at
   asl.ms speed 3 with ≥80% accuracy"), so "done with the unit" is a measurement,
   not a feeling.

## Lint

`python3 tools/verify.py --units` checks frontmatter fields, section order, and table
columns. `--links` checks every URL. Both must pass before a unit PR merges.
