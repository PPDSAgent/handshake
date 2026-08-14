# Delivery Checklist

Two deliveries, run separately. The computer-side learner goes first; the Lite-side
learner follows once Phase 6 exists. Everything here is a maintainer task — none of it
is delegable, and the two conversations at the end are the point of the whole project.

Check the boxes as you go. Anything you skip, write down why.

---

## Part A — Computer-side learner (Task 4.2)

### A1. Before you contact them

- [ ] **Provision the Claude account.** Create it, pay for it, and sign in *once*
      yourself so the first launch is a sign-in and not a signup. This is the single
      most likely install failure and it costs you five minutes to remove.
- [ ] **Confirm Mission 01's wording matches reality.** Open
      `install/INSTALL.md` Mission 01 and check the Claude Code install instructions
      against what the site actually says today. Vendors move buttons.
- [ ] **Decide the acquisition path** (Mission 00 supports both):
      - **Clone (default).** Requires the repo to be public, or a collaborator invite.
        `git pull` brings every curriculum update you ship afterward. Recommended.
      - **Tarball.** `bash tools/make_tarball.sh` → `dist/handshake-<date>.tar.gz`.
        Offline-capable and pleasingly physical on a USB stick, but it's a snapshot:
        updates mean sending a new tarball. Fine if you'd rather not make the repo
        public yet.
- [ ] **Know the push-guard answer before you're asked.** The clone path sets the push
      URL to `no_push_configured_see_INSTALL_Mission_05` so their practice data can
      never land in the public repo. They *will* notice. The answer: pulls work, that's
      the update channel; Mission 05 explains adding a private backup remote.
- [ ] **Run the real dry run** (Task 4.1) if it hasn't happened: follow `INSTALL.md`
      *exactly as written*, on a machine or user account with no dev toolchain, Missions
      00 through 03 including the boot ceremony. Mechanical path checks are already
      logged on the 4.1 issue; they are not a substitute for a human doing this cold.

### A2. Sending it

- [ ] Send the link (or the tarball) with **one** short message. Do not explain the
      system — `README.md` and the install manual do that, and explaining it in advance
      removes the part they'll enjoy.
- [ ] Say the one thing the docs can't: why you built it.
- [ ] Mention that Mission 05 exists. An engineer who knows there's a hood will open it.

### A3. Confirming it landed

- [ ] Ask for the Mission 02 checkpoint: the terminal showing `BOOTSTRAP COMPLETE` and
      `All clean.` A photo counts and they'll enjoy sending one.
- [ ] Confirm the boot ceremony wrote real values: `learners/current.txt` has their
      slug, their `profile.md` has a tutor name and a goal in their own words, and
      `state.md` shows `streak: 1`.
- [ ] **Schedule the first video call.** It doubles as unit 01's partner mission
      (fingerspell your name to each other, then read theirs back). Put it on a calendar
      before the conversation ends — "sometime soon" is how streaks die at day three.

**Done when:** their machine passed Mission 02 and they completed one session
unassisted. Not when you finished talking them through it.

---

## Part B — Lite-side learner (Task 4.3) — blocked until Phase 6 ships

- [ ] Confirm the Lite URL loads in the browser **on their actual tablet**, not yours.
- [ ] **Walk them through Add to Home Screen, live, on a call or in person.** This is
      their entire install. It happens once. There is no fallback and no one sitting
      next to them if it goes wrong. Do not send instructions and hope.
- [ ] Seed their name, goal, and track on first launch while you're still there.
- [ ] Sign the free Claude account in on the same tablet — that's their channel for
      asking questions the app can't answer.
- [ ] **Prove the relay end to end:** have them tap Export and text you the line, then
      paste it into `learners/shared/relay.md` and run `/checkin` to confirm it parses.
      A relay that's never been exercised is not a relay.

**Done when:** they complete one full drill session with nobody helping, and one relay
line has made the round trip. A guided demo is not evidence of an unguided second
session.

---

## Part C — After both are running

- [ ] **Week one:** check the streak, not the progress. Ask about the partner mission,
      not the vocabulary.
- [ ] **Ship curriculum updates by merging PRs**, then tell the clone-path learner to
      `git pull`. Tarball-path learners need a fresh tarball.
- [ ] **Watch for the unit-11 moment.** That unit pushes toward real Deaf community
      contact — local classes, Deaf events, Deaf-created media. If this project works,
      that's where it stops being a tutor and starts being a life change, and it's worth
      being ready to help with logistics when they get there.
- [ ] Keep the private mapping current. Names, ages, health context, and delivery
      logistics live in your own planning system — never in this repository.

---

## Standing rule

This repo is public. Nothing about a real learner — name, age, profession, health,
family detail — goes into a file, a commit message, an issue, or a PR. Learner
directories are created locally at install time and never pushed. If a change seems to
need a personal detail, it doesn't.
