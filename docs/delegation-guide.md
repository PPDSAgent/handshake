# Maintainer & Delegation Guide

How to execute this project with less expensive models doing the labor. The design
makes this safe: cheap models follow templates; machines verify links and formats;
you spot-check meaning. Total human time per delegated task: ~5 minutes.

## The loop

1. **Pick an issue.** Each GitHub issue = one plan task = one work session. Phase 1
   issues are independent — run several in parallel if you like.
2. **Dispatch.** Open a fresh Claude Code session in the repo on a cheap model
   (Haiku-class for Phases 1–2, Sonnet-class for 3, 4, and 6; see the plan's routing
   block). Prompt template:

   > Work task **<ID>** from `docs/superpowers/plans/2026-08-10-asl-tutor-buildout.md`.
   > Read the plan's Global Constraints and the task's full brief before touching
   > anything. Follow the steps exactly, including the verifier runs and the branch/
   > PR conventions. Paste `python3 tools/verify.py` output in the PR body. If you
   > cannot meet an acceptance criterion, stop and say so — do not improvise around it.

3. **Wait for CI.** The `verify` workflow re-runs the machine checks on the PR. Red
   CI = bounce it back to the model with the log; don't debug it yourself.
4. **Spot-check (the 5 minutes that matter).** Checklist below.
5. **Merge.** Update the issue. Done.

## Spot-check checklist (per PR)

- [ ] CI green **and** verify.py output pasted in the PR body (no output = no merge)
- [ ] Open 2 random source links — do they show the sign they claim? (CI proves
      *reachable*, only eyes prove *right* — this is the Source-or-Discard step)
- [ ] Any `NEEDS-HUMAN-EYES` flags resolved (SigningSavvy search URLs especially)
- [ ] Scan hooks/hints: nothing describes handshapes or movement (Rule 1)
- [ ] No health specifics or age-as-limitation language anywhere in the diff
- [ ] Read one section aloud in the learners' voices: would it land with two sharp
      adults who have built things for a living? No cheerleading, no condescension
- [ ] Phase 3 only: evidence numbers present (FPS, accuracy table) and honest-looking
- [ ] Phase 6 only: the PR names the actual device or viewport tested and the steps
      performed. "Should work on a tablet" fails this check — the Lite-side learner
      has no fallback and nobody sitting next to them

## Escalation rule

A cheap model fails a task twice → move that one task up a tier; don't move the
whole phase. Track nothing formally — the PR history is the record.

## Order of operations

**The computer-side learner ships first.** That decision (2026-08-11) exists to stop new scope from
delaying the thing that's nearly done. Phase 6 runs in parallel, not in front.

1. Phase 1 tasks 1.02–1.03 first (family units unblock real use), then the rest of
   Phase 1 in any order; Phase 2 anytime after. `/checkin` (2.4) should land before
   the Lite side starts relaying, since it's what reads the relay.
2. Phase 4.1 (dry run) before the computer-side delivery — non-negotiable; it's the install's
   only real test. 4.2 is that learner's handoff.
3. Phase 6 in parallel from the start, but 6.1 needs enough units built to be worth
   generating — dispatch it once Phase 1 is roughly half done. 6.1 → 6.2 → 6.3 → 6.4
   are strictly sequential. 4.3 is the Lite-side handoff and is blocked by all of Phase 6.
4. Phase 3 (webcam lab) after the computer-side learner is mid–unit-01 — a reward, not a
   distraction.
5. Phase 5 whenever curiosity strikes; it blocks nothing.

**Your one setup task in Phase 6:** hosting. GitHub Pages on this public repo,
free, ~10 minutes. Task 6.4 documents it and the Cloudflare Pages alternative.

## What NOT to delegate

- Anything touching `rules/tutor-rules.md` (the law is human-maintained)
- `curriculum/sources.md` allowlist changes (human browser check required)
- Anything that would put real names, ages, or health details in this public repo
- The two delivery conversations (4.2, 4.3) — those are yours. The Lite-side learner's
  Add-to-Home-Screen walkthrough especially: it is their entire install, it happens
  once, and it should happen with you on the call
