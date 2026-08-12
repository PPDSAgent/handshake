# HANDSHAKE — Field Installation Manual

**Classification: Family Business · Difficulty: trivial for you · Est. total time: 45–60 min**

You've been handed a personal AI tutor. It will teach you American Sign Language.
You will install it yourself, because whoever gave it to you knows you'd rather
assemble the thing than be handed it running.

Five missions plus one optional. Each ends with a **checkpoint** — a thing you can
observe that proves the mission succeeded. Engineers don't trust "it should work,"
and neither does this manual.

---

## Mission 00 — Acquire the payload

**Objective:** get the code onto your machine, survey the architecture.

**Path A — clone (recommended).** Your copy stays connected to the source: when the
curriculum grows, `git pull` brings the updates.

```bash
git clone https://github.com/PPDSAgent/handshake.git && cd handshake
```

(No git yet? Do Mission 01 step 1 first, then come back. The missions forgive
reordering; the checkpoints don't.)

**Path B — tarball.** If you were handed a `handshake-*.tar.gz` instead (no
internet, or ceremony — a tarball on a USB stick has a certain weight to it):

```bash
tar -xzf handshake-*.tar.gz && cd handshake
```

A tarball copy is a snapshot: it works fully offline after install, but updates
arrive as fresh tarballs, not `git pull`. Path A can be adopted later by cloning
and copying your `learners/<you>/` folder across — your data is just files.

Either path, then: look around (`ls -R | head -50` — it's all plain text) and read
`README.md` (2 minutes). Note the one rule that matters.

**Checkpoint:** you can state the one rule from README.md in your own words. (It's
about what the AI is *not* allowed to do.)

---

## Mission 01 — Toolchain

**Objective:** git, Python 3, and Claude Code installed and answering.

1. **git** — macOS: run `git --version` (it offers to install itself);
   Windows: https://git-scm.com → download installer.
2. **Python 3** — probably already present: `python3 --version`. If not:
   macOS `xcode-select --install` handles it; Windows: https://python.org installer
   (check "Add to PATH").
3. **Claude Code** — the AI runtime. Go to https://claude.com/claude-code and follow
   its install instructions for your platform (docs live at
   https://code.claude.com/docs if you want the long version). You'll need a Claude
   account — if one was set up for you, sign in with that; the tutor works with any
   paid plan.

**Checkpoint:** all three respond with version numbers:
```bash
git --version && python3 --version && claude --version
```
**If it breaks:** `claude: command not found` usually means a new terminal window is
needed (PATH updates don't apply to already-open shells).

---

## Mission 02 — Power-on self-test

**Objective:** prove the payload is intact before booting it.

From the `handshake/` directory:
```bash
bash install/bootstrap.sh
```
This checks your toolchain, sets up git history if you came in by tarball (a clone
already has one), and runs the system's own verifier, which live-checks every
lesson link against the internet.

**Checkpoint:** the script ends with `BOOTSTRAP COMPLETE` and the verifier reports
`All clean.`
**If it breaks:** the verifier names the exact file and URL it didn't like. A flaky
network can fail a link check — run it again before suspecting worse.

---

## Mission 03 — First contact

**Objective:** meet your tutor. Name it.

```bash
claude
```
When it greets you, say: **boot ceremony**

The tutor takes over from there. It will create your learner folder from the
template, ask you to name it (you're naming a thing you'll talk to daily — choose
wisely, no pressure), record your goal and your background, and walk you through
your first fingerspelling: your own name. That's real ASL, day one.

**Checkpoint:** `learners/current.txt` holds your slug;
`learners/<you>/profile.md` shows the tutor name you chose and your goal in your
own words; `learners/<you>/state.md` shows `streak: 1`. You made your first commit.

---

## Mission 04 — Establish the daily loop

**Objective:** make this a habit with the two commands you'll actually use.

- `/lesson` — learn the next chunk (15–20 min, the tutor watches the clock)
- `/drill` — review what's due (the spaced-repetition engine decides what)

Rules of engagement: short daily beats long weekly; when cards are due, drill before
lesson (the tutor will nag you correctly); missed days are logged without ceremony —
the streak just restarts.

**Checkpoint:** three consecutive days with journal entries in
`learners/<you>/journal.md`. After that the habit has a fighting chance.

---

## Mission 05 (optional) — Open the hood

**Objective:** confirm this is your machine, not an appliance.

- The spaced-repetition algorithm is ~10 lines of arithmetic documented in
  `learners/README.md`. Read it. Disagree with it. Change it — the tutor follows
  *your* version.
- Your entire learning history is one TSV: `learners/<you>/deck.tsv`. `grep` it,
  chart it, do terrible spreadsheet things to it.
- The verifier from Mission 02 is `tools/verify.py` — stdlib only, readable in one
  coffee.
- Your learner folder is *yours* and stays out of the public project — Mission 02
  disabled pushing toward the public repo entirely (pulls still work; that's your
  update channel). If you want your copy backed up off this machine, add a
  **private** repository of your own as a second remote:
  ```bash
  git remote add backup <your-private-repo-url> && git push -u backup main
  ```
  (The maintainer's undo for the push guard, should you ever contribute curriculum
  from this machine: `git remote set-url --push origin <url>` — but contributions
  are better made from a separate clone that has no learner data in it.)
- Coming attraction: a webcam rig that reads your fingerspelling using local
  hand-tracking (no cloud). It's on the build plan in `docs/`. You'll be the test
  pilot — and the calibration engineer.

**Checkpoint:** you've made one modification, however small, and committed it.

---

*Questions, bugs, or bragging: you know who to call. The builder would bet money on
you being at Mission 05 by day two.*
