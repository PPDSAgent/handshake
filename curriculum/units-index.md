# Units Index

Titles, statuses, and session estimates here are the authoritative record and must match
each unit file's frontmatter exactly — `tools/verify.py --index` enforces it.

| # | File | Title | Status | Est. sessions |
|---|---|---|---|---|
| 00 | `unit-00-boot-ceremony.md` | Boot Ceremony | built | 1 |
| 01 | `unit-01-fingerspelling.md` | The Alphabet Protocol | built | 6 |
| 02 | `unit-02-first-contact.md` | First Contact | built | 4 |
| 03 | `unit-03-family-network.md` | The Family Network | built | 4 |
| 04 | `unit-04-numbers-time.md` | Numbers & Time | built | 6 |
| 05 | `unit-05-daily-life.md` | Daily Life | built | 5 |
| 06 | `unit-06-questions-grammar.md` | Questions & Grammar I | built | 5 |
| 07 | `unit-07-feelings-health.md` | Feelings & Health | built | 4 |
| 08 | `unit-08-food.md` | Food & Restaurants | built | 4 |
| 09 | `unit-09-out-and-about.md` | Out & About | built | 4 |
| 10 | `unit-10-workshop.md` | Domain Vocabulary | built | 4 |
| 11 | `unit-11-deaf-culture.md` | Deaf Culture & Community | built | 3 |
| 12 | `unit-12-conversation-ops.md` | Conversation Ops | built | 6 |

**Total: 56 sessions** of 15–20 minutes — roughly three months at five a week, or a
little over four at three. (`tools/verify.py --index` adds the column and fails if this
number disagrees with it.) Unit 10 is track-split: its Learn section holds a shared base plus a
`workshop` and a `clinical` extension, and a learner is taught the base plus whichever
track their `profile.md` names.

`status` means: `draft` = being written · `built` = complete and machine-verified ·
`reviewed` = a maintainer has also spot-checked the links and prose by hand.

Progression rule: `/lesson` works the lowest non-complete unit per `learners/<learner>/state.md`.
Skipping ahead is allowed if they ask — it's their system — but the tutor says what it thinks.
