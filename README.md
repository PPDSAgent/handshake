# Handshake

**A personal ASL tutor that lives in your files — and is forbidden to hallucinate
signs.**

Every good protocol starts with a handshake. In American Sign Language, the word for
a hand's configuration is a *handshape*. This system teaches you the second by way of
the first: an AI tutor built from plain text files, git, and [Claude
Code](https://claude.com/claude-code) — no cloud account holding your data, no app
store, nothing you can't open in a text editor and tinker with. You will be
encouraged to tinker.

## The one rule that matters

Language models cannot reliably describe how to produce a sign, and wrong motor
memory is expensive to unlearn. So the AI here **never teaches a sign from its own
memory**. It sequences, drills, quizzes, schedules, and keeps you honest; the signs
themselves are taught by linked videos from vetted, mostly Deaf-created sources
([curriculum/sources.md](curriculum/sources.md)) — Lifeprint/ASL University,
Handspeak, SigningSavvy, asl.ms. If the tutor ever describes a sign's handshape from
memory, that's a bug — file it.

## Who this is for

It was built inside one family for a pair of learners learning together — one who
wanted to assemble the thing, one who wants an appliance that just works — and
then opened up in case your family can use it too. The design
assumes adults, short daily sessions, and ideally a **partner**: two people learning
together retain more, and the shared missions in
[learners/shared/missions.md](learners/shared/missions.md) are the point of the whole
exercise.

## What's in the box

| Path | What it is |
|---|---|
| `CLAUDE.md` | The tutor's brain — Claude Code reads this every session |
| `rules/` | The tutor's law (Rule 1 is the one above) |
| `curriculum/` | 12 units, from fingerspelling to real conversation |
| `learners/` | One folder per person — deck, streak, journal, all plain files. Ships as a template; the Boot Ceremony creates yours |
| `.claude/skills/` | `/lesson` and `/drill` — the two commands you'll actually use |
| `tools/` | `verify.py` (link + data + prose checks), `make_tarball.sh` (offline packaging) |
| `install/` | **Start here** → [install/INSTALL.md](install/INSTALL.md) |
| `docs/` | Design spec, build plan, maintainer guide |

## Quick start

You need git, Python 3, and [Claude Code](https://claude.com/claude-code) with a paid
Claude plan (the install manual walks through all three):

```bash
git clone https://github.com/PPDSAgent/handshake.git
cd handshake && claude
```

Then say **"boot ceremony"**. The tutor takes it from there — including asking you
what its name should be.

## Handshake Lite (in build)

For the partner who won't touch a terminal: a tap-to-drill web app for a tablet —
no account, no install beyond Add to Home Screen, progress kept on-device with the
same scheduling algorithm. It's Phase 6 of the [build
plan](docs/superpowers/plans/2026-08-10-asl-tutor-buildout.md); until it ships, the
computer-side tutor runs solo missions.

## Contributing

Welcome — especially curriculum units and source vetting. Read
[CONTRIBUTING.md](CONTRIBUTING.md) first: this project has one non-negotiable law
(above) and a verifier that enforces what can be enforced mechanically. All sign
content is **linked, never copied** — the educators who made it earn their living
from their sites.

## License

MIT — see [LICENSE](LICENSE). The linked lesson content belongs to its creators and is
not part of this repository; [NOTICE.md](NOTICE.md) explains that boundary and why it's
a design constraint rather than an oversight.
