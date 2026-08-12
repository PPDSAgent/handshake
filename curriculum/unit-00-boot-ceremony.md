---
unit: 0
title: Boot Ceremony
status: built
est_sessions: 1
---

# Unit 00 — Boot Ceremony

## Why this unit

You just built a machine that teaches language. Before it teaches you anything, it
needs three things only you can provide: its name, your goal, and your name — spelled
the way you'll soon spell it with one hand. This unit is one session, and by the end
of it you'll have configured the system *and* produced your first ASL.

## Watch

- https://www.lifeprint.com/asl101/fingerspelling/fingerspelling.htm — the
  fingerspelling landing page at ASL University (free curriculum by Dr. Bill Vicars,
  a Deaf professor). Skim the intro and find the alphabet chart; ~5 minutes. Unit 01
  goes deep here — today is just reconnaissance.

## Learn

| sign | source | hook |
|---|---|---|
| HELLO | https://www.lifeprint.com/asl101/pages-signs/h/hello.htm | your opener for every session and every conversation |
| NAME | https://www.lifeprint.com/asl101/pages-signs/n/name.htm | the first question Deaf people will ask you |
| ME | https://www.lifeprint.com/asl101/pages-signs/m/me.htm | pairs with NAME: "MY NAME…" — your first sentence |

## Drill

When this unit opens, `/lesson` appends to the deck:

- One `vocab` card per Learn row above (prompts: "Sign: HELLO", "Sign: NAME",
  "Sign: ME").
- One `fingerspell` card: "Fingerspell your own first name" (source: the
  fingerspelling landing page above).

## The ceremony itself (tutor: run this interactively)

1. **Create the learner.** Ask who's at the keyboard, agree on a short lowercase
   slug, then: copy `learners/_template/` to `learners/<slug>/`, set `learner:` and
   `display_name:` in the new `profile.md`, and write the slug to
   `learners/current.txt` — one line, no punctuation (gitignored: it describes this
   machine, not the repo).
2. **Name the tutor.** Offer Ada, Hopper, Marconi, Tesla — or anything they like
   better. Write it to `tutor_name` in their `profile.md`.
3. **Capture the goal and the background.** One sentence each, their words, into
   `goal` and `background` in `profile.md`. ("Understand my family at Sunday
   dinner" beats "learn ASL"; "forty years building radios" tells the tutor how to
   teach.) Set `track` and `partner` while you're in there.
4. **First transmission.** Using the alphabet chart from Watch, they fingerspell their
   first name — slowly, letter by letter, checking each against the chart. The tutor
   does not correct handshapes from memory (Rule 1); the chart is the referee.
5. **Commit.** `git add -A && git commit -m "boot: system configured"` — their first
   commit to their own learning system. Then set `current_unit: 1` and `streak: 1` in
   `state.md`.

## Family mission

Tell one family member the tutor's name and your goal — by text, call, or in person.
Announcing a project makes it real. (They may want in. Let them.)

Learning with a partner? `learners/shared/missions.md` has the two-person version of
this and every later unit's mission.

## Checkpoint

- [ ] `learners/current.txt` names the learner; `profile.md` has a tutor name and a
      goal in their own words; `state.md` shows streak: 1
- [ ] They fingerspelled their first name against the chart without skipping letters
- [ ] First git commit exists
- [ ] They know the one rule: the tutor links, the videos teach
