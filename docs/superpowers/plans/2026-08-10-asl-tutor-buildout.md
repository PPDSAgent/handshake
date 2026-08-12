# Handshake Build-Out Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Each task is also mirrored as a GitHub issue — one issue = one work session = one PR.

**Goal:** Complete the Handshake ASL tutor from its Phase-0 skeleton (units 00–01,
/lesson, /drill, verifier, installer, paired-learner layer) to a full 12-unit
curriculum with supporting skills, a webcam fingerspelling lab, a delivery-tested
install for the computer-side learner, and an account-free tablet app for the Lite-side learner.

**Architecture:** Markdown-first Clark-OS pattern. Curriculum = data (unit files),
skills = behavior (SKILL.md), learner state = TSV + markdown under `learners/<slug>/`.
The AI never teaches sign production; allowlisted videos do. `tools/verify.py` is the
machine gate; the maintainer's spot-check is the human gate.

**Tech Stack:** Markdown, git, Claude Code skills, Python 3 stdlib (verifier and the
Lite generator), vanilla HTML/CSS/JS (Phase 6 — no framework), Python + MediaPipe +
OpenCV (Phase 3 only, in a venv).

**Read first:** `docs/superpowers/specs/2026-08-10-asl-tutor-design.md` (v1.2) for the
two-learner model, and `learners/README.md` for the SRS algorithm and relay design.

**Loop header (per clark `rules/model-routing.md` — governs every dispatch from this
plan):**
- **Goal:** a delivered, verified tutor for the computer-side learner, then the Lite
  app for the partner — built by cheap models against these briefs.
- **Verifier:** `python3 tools/verify.py` exit 0 + CI green + the maintainer's per-PR
  spot-check (`docs/delegation-guide.md`); each task's own acceptance evidence.
- **Step size:** one task = one branch = one PR; no task starts before its
  blockers merge.
- **Stop:** stop a task after two failed attempts at its acceptance criteria and
  escalate one model tier (delegation guide, Escalation rule); stop the phase and
  surface to the maintainer if the same task fails at the higher tier.

**Routing note (recorded per model-routing):** Phase 0's reference implementation
(units 00–01, skills, verifier) was deliberately built on Judgment-tier models —
it is the template every cheap-model task copies, so its quality bounds the fleet's.
Phases 1–2 run Haiku-class by design from here on.

## Global Constraints

Every task inherits these. Verbatim from the spec and `rules/tutor-rules.md`:

- **Never describe how to produce a sign** in any file — no handshape/movement/
  orientation descriptions. Hooks and hints address meaning and context only.
- **Link, never copy.** No text, images, or transcripts from source sites enter the repo.
- **Allowlist-only URLs** (`curriculum/sources.md`). Verified patterns:
  `lifeprint.com/asl101/pages-signs/<initial>/<word>.htm`,
  `signingsavvy.com/search/<word>`, `handspeak.com` entry pages, `asl.ms`,
  `youtube.com/billvicars`. A pattern-shaped URL is not a verified URL — every link
  must pass `python3 tools/verify.py --links` from *your* machine before commit.
- **`python3 tools/verify.py` exits 0** before any commit is pushed. Paste its output
  in the PR body — an unverified "it passes" claim is treated as false (Iron Law).
- **Stdlib-only** for anything under `tools/` that the install runs. Phase 3 code
  lives in `lab/` with its own venv and never becomes an install dependency.
- **This is a PUBLIC repository. No personal data of any real learner, anywhere.**
  No real names, ages, health specifics, or family details — in
  files, commit messages, issues, PR bodies, or examples. Learner directories are
  created locally from `learners/_template/` at install time and are never pushed
  here. Example names in docs are fictional. If a task seems to need a personal
  detail, it doesn't — personal logistics live in the maintainer's private
  planning system.
- **One algorithm, two implementations.** The SRS spec in `learners/README.md` is
  normative for both `/drill` and Handshake Lite. Changing scheduling behavior in one
  without the other is a defect, not an improvement.
- **Tone:** colleague-to-colleague, dry, zero condescension. Handshake's first
  learners are sharp adults learning late in life. If a sentence would land wrong
  said to a sharp colleague, rewrite it. Never reference age except as an asset.
- **One task = one branch = one PR.** Branch `task/<id>-<slug>`. Commit message
  prefix `feat(unit-07):` / `feat(skill-quiz):` etc.

**Model routing** (mirrors clark `rules/model-routing.md`): Phase 1 and 2 tasks are
template-following — cheapest available tier (Haiku-class) is expected to succeed;
escalate one tier only on observed failure. Phase 3–4 need judgment — Sonnet-class.
Review is always the maintainer (human), assisted by CI.

---

## Phase 1 — Curriculum build-out (11 tasks, one per unit)

Eleven instantiations of the same fully-specified task. **The template below is the
complete task**; the table supplies each instantiation's parameters. Reference
implementations: `curriculum/unit-00-boot-ceremony.md` and
`curriculum/unit-01-fingerspelling.md` — match their voice and structure exactly.
Format law: `curriculum/README.md`.

### Task 1.N template — Build unit NN

**Files:**
- Create: `curriculum/unit-NN-<slug>.md` (exact filename from `curriculum/units-index.md`)
- Modify: `curriculum/units-index.md` (status `planned — Phase 1` → `built`)

**Interfaces:**
- Consumes: unit format spec (`curriculum/README.md`), allowlist (`curriculum/sources.md`)
- Produces: a unit file `/lesson` can run unmodified — Drill section must name card
  types from `learners/README.md` (`vocab` | `fingerspell` | `phrase`)

**Steps:**

- [ ] **Step 1: Read the three law files.** `curriculum/README.md`,
  `rules/tutor-rules.md`, and reference unit `unit-01-fingerspelling.md`. Do not
  start writing before all three.
- [ ] **Step 2: Resolve the vocabulary.** Start from the candidate list in the
  parameter table. For each word, find its page: try
  `https://www.lifeprint.com/asl101/pages-signs/<first-letter>/<word>.htm` first;
  if that 404s, use `https://www.signingsavvy.com/search/<word>`. Drop or substitute
  words you cannot source — 8 well-sourced signs beat 12 shaky ones. **Search-URL
  caveat:** SigningSavvy search pages return HTTP 200 even for missing words, so for
  every search URL you must confirm the word actually has results (fetch the page and
  check, or flag it `NEEDS-HUMAN-EYES` in the PR body for the maintainer).
- [ ] **Step 3: Draft the unit** — all six required sections in order, frontmatter
  `status: draft`, `est_sessions` from the table. Why-this-unit ties to real
  conversations the learners want to have with each other and their family. Hooks =
  meaning/context only. Family mission ≤10 minutes, involves one other person,
  concrete. Write for two learners, not one: no "his", no assumption about which
  surface they're on.
- [ ] **Step 4: Run the verifier.**
  ```bash
  python3 tools/verify.py
  ```
  Expected: `All clean.` Fix every finding; re-run until exit 0.
- [ ] **Step 5: Self-review against the rejection list.** Reject your own draft if:
  any hook describes production; any URL is pattern-guessed but unverified; tone
  drifts into cheerleading; more than 15 signs; any section missing. Fix, then
  set frontmatter `status: built` and update `units-index.md`.
- [ ] **Step 6: Commit and open PR.**
  ```bash
  git checkout -b task/1-NN-<slug>
  git add curriculum/ && git commit -m "feat(unit-NN): <title>"
  git push -u origin task/1-NN-<slug>
  gh pr create --title "Unit NN: <title>" --body "<verify.py output pasted here + any NEEDS-HUMAN-EYES flags>"
  ```
  Expected: CI `verify` job green on the PR.

**Parameter table (one row = one task = one issue):**

| Task | Unit file | est_sessions | Candidate vocabulary (verify each; drop what you can't source) |
|---|---|---|---|
| 1.02 | `unit-02-first-contact.md` | 4 | NICE-TO-MEET-YOU, THANK-YOU, PLEASE, SORRY, YES, NO, GOOD, BAD, GOODBYE, AGAIN, SLOW (AGAIN + SLOW are survival tools for a new signer — say so) |
| 1.03 | `unit-03-family-network.md` | 4 | FAMILY, MOTHER, FATHER, WIFE, HUSBAND, SON, DAUGHTER, BROTHER, SISTER, GRANDMOTHER, GRANDFATHER, LOVE |
| 1.04 | `unit-04-numbers-time.md` | 5 | numbers 1–20 (Lifeprint has dedicated number pages — find and link them), TIME, DAY, WEEK, MONTH, YEAR, TODAY, TOMORROW, YESTERDAY |
| 1.05 | `unit-05-daily-life.md` | 5 | HOME, EAT, DRINK, SLEEP, WORK, HELP, WANT, NEED, GO, COME, BATHROOM |
| 1.06 | `unit-06-questions-grammar.md` | 5 | WHO, WHAT, WHERE, WHEN, WHY, HOW, UNDERSTAND, KNOW, QUESTION — plus Watch links covering non-manual markers (eyebrow grammar); Lifeprint has lesson pages on WH-questions. This unit is concept-heavy: 2 extra Watch links allowed |
| 1.07 | `unit-07-feelings-health.md` | 4 | HAPPY, SAD, ANGRY, TIRED, SICK, HURT/PAIN, DOCTOR, MEDICINE, FEEL, DEAF, HARD-OF-HEARING, HEARING — the identity trio matters here; place it prominently and connect it forward to unit 11. Keep the framing factual and outward-looking (these are signs you will see and need), not personal |
| 1.08 | `unit-08-food.md` | 4 | WATER, COFFEE, TEA, MILK, BREAD, CHICKEN, FISH, HUNGRY, THIRSTY, RESTAURANT, FINISH |
| 1.09 | `unit-09-out-and-about.md` | 4 | STORE, BUY, MONEY, COST, CAR, DRIVE, WALK, STOP, OUTSIDE, WHERE (review-link back to 06) |
| 1.10 | `unit-10-workshop.md` | 4 | **Track-split unit — see the note below.** Shared base: WORK, MAKE, BUILD, FIX/REPAIR, IDEA, PLAN, PROBLEM, MACHINE. Then two extension tables: `workshop` (COMPUTER, PHONE, TOOL, METAL, WOOD, ELECTRICITY) and `clinical` (TEETH, DENTIST, PAIN, APPOINTMENT, CLEAN, PATIENT). The Why-section should say plainly: this is the vocabulary of *your* world, and the two of you have different ones |
| 1.11 | `unit-11-deaf-culture.md` | 3 | DEAF, HEARING, SIGN, LANGUAGE, INTERPRETER, CULTURE — plus Watch links: Handspeak culture articles, https://www.nad.org/ community/local-resources pages. Etiquette content (attention-getting, eye contact, name signs) via links, not prose summaries |
| 1.12 | `unit-12-conversation-ops.md` | 6 | Mostly `phrase` cards built from prior units (HOW-ARE-YOU, MY NAME __, etc. — source each phrase page from Lifeprint lessons); exit retest: repeat unit 01's asl.ms checkpoint and compare speed to the baseline logged in `state.md`; sustained family ritual as the closing mission |

**Note on the track-split unit (1.10 only).** Unit 10 carries three tables instead of
one: `## Learn` holds the shared base, then `### Track: workshop` and
`### Track: clinical` hold six signs each. `/lesson` reads the learner's `track` from
their `profile.md` and teaches the base plus that one extension; Handshake Lite does
the same. The unit lint expects the standard six sections, so the track tables live
*inside* `## Learn` as subsections — do not add new top-level sections.

**Sequencing:** 1.02 and 1.03 first (they unblock real family use), then any order.
All tasks independent — parallelizable across workers.

---

## Phase 2 — Skills roster (4 tasks)

Reference implementations: `.claude/skills/lesson/SKILL.md` and
`.claude/skills/drill/SKILL.md`. Match their structure: frontmatter (name +
trigger-rich description), procedure numbered, session-close = journal + state +
commit offer. All skills obey `rules/tutor-rules.md` and end sessions on time.

### Task 2.1: /quiz — checkpoint runner

**Files:** Create `.claude/skills/quiz/SKILL.md`

**Interfaces:** Consumes unit Checkpoint sections + `learners/<learner>/state.md`;
produces pass/fail per checkpoint item written to the journal, and (all-pass)
`current_unit` bump — the same unit-complete protocol `/lesson` uses; the two must
not disagree, so this skill states it defers to `/lesson`'s protocol text.

- [ ] Write SKILL.md: procedure = load current unit checkpoint → run each item as a
  live measurement (asl.ms run, timed A–Z, video-call read) → record evidence per
  item ("measured", never "they say they can") → all-pass = bump unit + one plain
  congratulation; any-fail = that item becomes journal `next:` → close per Rule 4.
- [ ] Dry-run it in a Claude Code session against unit 01 with fabricated learner
  answers; transcript must show: no production descriptions, evidence recorded per
  item, correct state.md handling. Paste transcript excerpt in PR.
- [ ] `python3 tools/verify.py` → exit 0. Commit `feat(skill-quiz)`, PR.

### Task 2.2: /report — progress report

**Files:** Create `.claude/skills/report/SKILL.md`

**Interfaces:** Consumes `deck.tsv`, `journal.md`, `state.md`. Produces a terminal
report; never modifies state.

- [ ] Write SKILL.md: report = streak, unit position, deck stats (cards total/due/
  retired = interval ≥21d), asl_ms_speed trend from journal history, misses-by-card
  leaderboard ("your nemeses"), one recommendation. Numbers computed from the files,
  not estimated — show the arithmetic on request. Engineer-dashboard tone.
- [ ] Dry-run with a hand-built 10-row deck.tsv fixture (in the session, not
  committed); verify counts match the fixture by hand. Paste transcript excerpt in PR.
- [ ] `python3 tools/verify.py` → exit 0. Commit `feat(skill-report)`, PR.

### Task 2.3: /coach — free-form Q&A under the law

**Files:** Create `.claude/skills/coach/SKILL.md`

**Interfaces:** Consumes `rules/tutor-rules.md`, `curriculum/sources.md`. May append
`lookup` cards to `deck.tsv` (schema per `learners/README.md`).

- [ ] Write SKILL.md: handles "how do I sign X?" (allowlist lookup together — **open
  the page with the learner and confirm the sign is actually there before adding the
  card; a search URL returns HTTP 200 even for words the dictionary does not have**,
  per Rule 3 — then offer the `lookup` card), "why does ASL do Y?" (concept coaching
  from model knowledge is allowed — grammar/culture/learning-strategy, citing unit 11
  where covered), and "I'm stuck/frustrated" (shrink session per Rule 5). Must include
  the Rule 1 self-catch protocol verbatim concept: stop mid-sentence, say so, link.
- [ ] Dry-run: ask it "how do I sign REFRIGERATOR?" — transcript must show lookup
  flow, not description. Ask "why do signers raise eyebrows?" — concept answer
  allowed. Paste both excerpts in PR.
- [ ] `python3 tools/verify.py` → exit 0. Commit `feat(skill-coach)`, PR.

### Task 2.4: /checkin — weekly review, partner missions, and the relay

**Files:** Create `.claude/skills/checkin/SKILL.md`

**Interfaces:** Consumes the learner's `journal.md` (last 7 days) and `state.md`,
`learners/shared/missions.md`, and `learners/shared/relay.md`. Produces a weekly
journal entry `## <date> — weekly checkin`, an updated mission log, and — when a new
relay line is present — an updated `state.md` for the relaying learner (their
directory created from `learners/_template/` the first time their name appears).

- [ ] Write SKILL.md, three parts:
  **(a) Weekly review** — wins from the journal (concrete, quoted), streak health
  (misses without guilt), next week's one focus, and from unit 11 on, a nudge toward
  a local Deaf community event (NAD link from `sources.md`).
  **(b) Partner mission** — read `learners/shared/missions.md`, report the current
  unit's mission status, and if it's unstarted, book it: ask for a real day and time,
  then write it into the Log section. Completed missions get a dated line plus one
  sentence on how it actually went.
  **(c) Relay** — read the newest line per learner in `learners/shared/relay.md`.
  First sight of a new name: copy `learners/_template/` to `learners/<slug>/`, set
  `surface: lite` and `last_relay` in the new files. If a line is newer than that
  learner's `last_relay`, parse it and update their `current_unit`, `streak`,
  `asl_ms_speed`, and `last_relay`. **Report every field you could not parse rather
  than inferring it** — a malformed line means "ask", not "guess". If the newest
  line is older than 14 days, say their status is unknown; never report a stale
  streak as current, and never characterize a gap as the learner having stopped.
- [ ] Dry-run against a fabricated week of journal entries plus two relay lines, one
  well-formed and one with a mangled field. Transcript must show: real entries quoted,
  a concrete mission booked, the good line parsed into state, and the bad line
  reported rather than guessed. Paste excerpts in PR.
- [ ] `python3 tools/verify.py` → exit 0. Commit `feat(skill-checkin)`, PR.

---

## Phase 3 — Webcam fingerspelling lab (3 tasks, sequential)

Sonnet-tier. Python in `lab/` with venv; **never** an install dependency for the
core tutor. The tinkerer is the intended co-developer — code must be readable, commented at
the "smart engineer, new to CV" level, with calibration knobs deliberately exposed.

### Task 3.1: Landmark capture spike

**Files:** Create `lab/README.md`, `lab/requirements.txt` (`mediapipe`,
`opencv-python` — pin exact versions that install cleanly on macOS AND Windows the
day you build this), `lab/capture.py`

**Interfaces:** Produces `get_landmarks(frame) -> list[21 (x,y,z)] | None` in
`capture.py`, imported by Task 3.2.

- [ ] `lab/README.md`: venv setup (`python3 -m venv .venv && source .venv/bin/activate
  && pip install -r requirements.txt`, plus Windows variant), what MediaPipe Hands is
  (one paragraph, link https://ai.google.dev/edge/mediapipe/solutions/guide), privacy
  note: all local, nothing leaves the machine.
- [ ] `capture.py`: webcam preview window with the 21 hand landmarks drawn live;
  `q` quits; prints FPS to console; exposes `get_landmarks(frame)`.
- [ ] Verify on a real webcam: landmarks track your hand at ≥15 FPS. Record the FPS
  number in the PR. (No webcam in your environment → the task blocks; say so rather
  than faking it — Iron Law.)
- [ ] Commit `feat(lab): landmark capture spike`, PR with FPS evidence.

### Task 3.2: Calibrated letter classifier

**Files:** Create `lab/classify.py`, `lab/calibrate.py`; data file
`lab/calibration.json` (gitignored — add `lab/calibration.json` + `lab/.venv/` to
`.gitignore` in this task)

**Interfaces:** Consumes `get_landmarks` from 3.1. Produces
`classify(landmarks) -> (letter: str, confidence: float)` over the 24 static
letters (J and Z excluded — motion letters; the UI must say "J/Z: not in v1" when
asked, not fail silently).

- [ ] `calibrate.py`: guided flow — for each of 24 letters, shows the letter (text
  prompt referencing the Lifeprint chart URL for self-check), captures 3 samples of
  normalized landmarks (wrist-origin, scale-normalized), writes `calibration.json`.
  Restartable per letter; the learner IS the training data — say so in the prompts,
  it's the fun part.
- [ ] `classify.py`: k-NN (k=3) over calibration samples, cosine distance,
  confidence = mean similarity; below-threshold → "unsure" rather than a wrong
  letter (threshold a named constant at the top with a comment inviting tuning).
- [ ] Self-test protocol in `lab/README.md`: calibrate, then run 24-letter self-test
  twice; report per-letter accuracy table. Acceptance: ≥80% overall on the author's
  own hands, honestly reported in the PR (include the table).
- [ ] Commit `feat(lab): calibrated static-letter classifier`, PR with accuracy table.

### Task 3.3: Fingerspelling drill game

**Files:** Create `lab/spell_drill.py`; Modify `lab/README.md` (usage),
`.claude/skills/drill/SKILL.md` (add one line offering the lab as an alternative
receptive/expressive block when installed)

**Interfaces:** Consumes `classify` from 3.2. Produces a terminal+window game loop.

- [ ] `spell_drill.py`: word list (start: the 100 most common English 3–6 letter
  words, embedded as a Python list — no external file), prompts a word, reads
  letters via classifier with a hold-to-confirm dwell (letter stable for ~1s =
  accepted, avoids flicker), shows per-word time + accuracy, session summary at the
  end. Skips J/Z words automatically (documented).
- [ ] Play 10 words on camera; PR includes the session summary output.
- [ ] `python3 tools/verify.py` → exit 0 (deck/units untouched but run it anyway —
  it's the habit). Commit `feat(lab): fingerspelling drill game`, PR.

---

## Phase 4 — Packaging & delivery (2 tasks)

### Task 4.1: Fresh-machine install dry run

**Files:** Modify `install/INSTALL.md` (friction fixes found); Create
`docs/dry-run-log.md`

- [ ] Build the tarball: `bash tools/make_tarball.sh` (needs clean tree).
- [ ] On a machine/account with NO dev toolchain (new macOS user account is the
  cheap option), follow `install/INSTALL.md` **exactly as written** — Missions 00
  through 03, no improvising. Log every deviation, ambiguity, or failure with
  timestamps in `docs/dry-run-log.md`.
- [ ] Every INSTALL.md checkpoint must pass as literally written, including the boot
  ceremony writing real values to `state.md`. Any checkpoint that needs
  interpretation = a bug; fix INSTALL.md in the same PR.
- [ ] Human gate (maintainer): review the friction log before delivery. Commit
  `fix(install): dry-run findings`, PR.

### Task 4.2: Delivery package — computer-side learner

**Files:** Create `docs/delivery-checklist.md`

- [ ] Checklist contents: choose the acquisition path with the learner — **clone
  (default; the public repo gives read access with no invitation, and `git pull`
  brings updates)** or a ceremonial tarball from post-dry-run main (a snapshot:
  updates arrive as fresh tarballs — INSTALL.md Mission 00 states the trade
  honestly, and `bootstrap.sh` handles both). Provision and sign in the learner's
  paid Claude account **before** delivery, then confirm Mission 01's wording
  matches what they'll actually see (sign-in, not signup). Note in the checklist:
  the learner's own progress never pushes to the public repo — Mission 05 covers a
  private backup remote if they want one. Printed one-pager optional (the README
  quick start fits on one page). Schedule the first video call, which doubles as
  the unit-01 partner mission.
- [ ] The maintainer executes the checklist. Done when the learner's machine passes
  Mission 02's checkpoint — confirmation from the horse's mouth (a photo of
  `BOOTSTRAP COMPLETE` counts; they'll enjoy sending it).

### Task 4.3: Delivery package — Lite-side learner (blocked by Phase 6)

**Files:** Modify `docs/delivery-checklist.md` (add a second section)

- [ ] Checklist contents: confirm the Lite URL loads in the browser on *their*
  tablet; walk them through **Add to Home Screen** in person or on a video call —
  this is the single step most likely to fail unattended, and it is the whole
  install; seed their name and
  goal on first launch; confirm the free Claude account signs in on the same iPad for
  questions; show them the Export button once and text one line back so the relay is
  proven end to end.
- [ ] Done when they complete one full drill session unassisted and one relay line
  reaches `learners/shared/relay.md`. Do not mark this complete on a demo — an
  assisted first session is not evidence of an unassisted second one.

---

## Phase 5 — Stretch: local-model path (1 task, honesty-gated)

### Task 5.1: Ollama feasibility verdict

**Files:** Create `docs/local-model-verdict.md`

- [ ] Install Ollama (https://ollama.com/), pull 2–3 small instruct models that fit
  a consumer machine.
- [ ] Test each against the tutor job: give it `CLAUDE.md` + `rules/tutor-rules.md` +
  unit 01 and run a scripted lesson + drill. Score: Rule-1 compliance under
  pressure ("just describe the sign for me" ×5 phrasings), session-shape adherence,
  file-update correctness (deck row arithmetic), tone.
- [ ] Write the verdict: viable/not-viable per model, with transcript evidence, and
  what it would take (harness, guardrails) to run Handshake fully local. **"Not good
  enough yet" is an acceptable and expected conclusion** — the deliverable is the
  evidence, not a yes.

---

## Phase 6 — Handshake Lite: the iPad app (4 tasks, sequential)

The Lite-side learner's entire surface. Sonnet-tier — judgment work, not template-filling.

**Non-negotiables for every task in this phase.** The Lite-side learner will not
tinker, and there is no one sitting next to them when it breaks:

- **Zero setup, zero account, zero network writes.** If a step requires typing a URL
  twice, it has failed.
- **Vanilla HTML/CSS/JS.** No framework, no bundler, no npm, no CDN. The whole app is
  a handful of files served statically, so it still works in five years.
- **Accessibility is functional, not cosmetic:** base font ≥20px, tap targets ≥48px,
  WCAG AA contrast in both orientations, no timed interactions, no hover-only
  affordances, no gesture that isn't also a button.
- **Rule 1 binds here too.** The app links to videos; it never renders a description
  of how to make a sign.
- **The algorithm is copied, not reinvented** — `learners/README.md` is normative.

### Task 6.1: Curriculum → data generator

**Files:** Create `tools/build_lite.py`; Modify `.github/workflows/verify.yml` (run
the generator, fail the build if it errors)

**Interfaces:** Produces `lite/data.json` (gitignored — generated, never hand-edited)
with shape:
```json
{"generated":"YYYY-MM-DD",
 "units":[{"unit":1,"title":"…","est_sessions":6,"why":"…",
           "watch":[{"url":"…","note":"…"}],
           "learn":[{"sign":"HELLO","source":"https://…","hook":"…","track":null}],
           "drill":["Sign: HELLO"],"mission":"…","checkpoint":["…"]}],
 "missions":[{"unit":1,"text":"…"}]}
```
`track` is `null` for base rows, `"workshop"` or `"clinical"` for unit 10's extensions.

- [ ] Write the generator: stdlib only, parses unit frontmatter and the six sections,
  parses `learners/shared/missions.md` for the partner missions, writes `lite/data.json`.
- [ ] It must **fail loudly** on any unit it cannot parse — a silently skipped unit is
  a lesson the Lite-side learner never sees. Exit non-zero with the filename and the section that broke.
- [ ] Verify: run it against the current curriculum, confirm units 00 and 01 round-trip
  with every field populated and no empty strings. Paste the unit-01 JSON in the PR.
- [ ] `python3 tools/verify.py` → exit 0. Commit `feat(lite): curriculum generator`, PR.

### Task 6.2: The app shell

**Files:** Create `lite/index.html`, `lite/app.js`, `lite/style.css`,
`lite/manifest.webmanifest`, `lite/sw.js`, `lite/icon-192.png`, `lite/icon-512.png`

**Interfaces:** Consumes `lite/data.json` from 6.1. Produces the four screens and the
localStorage schema `handshake.<learnerSlug>` = `{profile, cards[], history[]}` where
`cards[]` mirrors the TSV columns from `learners/README.md`.

- [ ] Build four screens: **Today** (due count, one big Start button) · **Card**
  (prompt, a "Show me the sign" button opening the source URL in a new tab, then three
  grade buttons) · **Progress** (streak, cards total/due/retired, current unit) ·
  **Missions** (the current unit's partner mission, with a done checkbox).
- [ ] First-launch flow: ask for a name and a goal, offer the tutor-name choice (Ada,
  Hopper, Marconi, Tesla), pick a track. Four taps, then straight into a lesson.
- [ ] Learner switcher: multiple profiles per device, each its own localStorage key,
  switchable from Progress. This is what lets one family tablet hold test profiles for
  the grandkids without touching the primary learner's data.
- [ ] Manifest + service worker so **Add to Home Screen** yields a full-screen app that
  opens offline (cached shell + data.json; video links obviously need network).
- [ ] Verify on a real iPad or Safari responsive mode at iPad dimensions: add to home
  screen, launch from the icon, complete one card, force-quit, relaunch, confirm
  progress survived. Paste the steps you actually performed in the PR — "should work"
  is not evidence.
- [ ] Commit `feat(lite): app shell`, PR.

### Task 6.3: SRS parity test

**Files:** Create `lite/srs.js` (extracted scheduling logic), `tools/test_srs_parity.py`

**Interfaces:** `lite/srs.js` exports `review(card, grade) -> card`. The Python test
implements the same spec independently and asserts both agree.

- [ ] Extract scheduling out of `app.js` into `srs.js` as one pure function.
- [ ] Write `tools/test_srs_parity.py`: runs a fixed 30-step grade sequence
  (`miss/got it/easy` in a deterministic pattern) through the Python reference
  implementation of `learners/README.md` **and** through `srs.js` via `node`, then
  asserts `ease`, `interval_days`, `due`, `reps`, and `lapses` match at every step.
  Skip with a clear message (not a failure) if `node` isn't installed.
- [ ] Verify: run it, paste the passing output. Then deliberately change one constant
  in `srs.js`, confirm the test fails, and revert. Paste both outputs — a test not
  observed failing is not known to work.
- [ ] `python3 tools/verify.py` → exit 0. Commit `feat(lite): SRS parity test`, PR.

### Task 6.4: Hosting and the relay export

**Files:** Modify `lite/app.js` (Export + Backup buttons); Create `lite/README.md`

**Interfaces:** Export emits exactly the one-line format specified in
`learners/README.md` §Relay. Backup emits the full profile + cards as JSON.

- [ ] Export button: builds the line, copies it to the clipboard, **and** shows it in
  a selectable text box (clipboard permissions are unreliable in iOS standalone mode —
  the visible text is the real mechanism, the clipboard is the convenience).
- [ ] Backup button: downloads `handshake-<name>-<date>.json`. Import counterpart that
  restores it, because a backup you can't restore isn't one — verify the round trip.
- [ ] `lite/README.md`: how to deploy. Primary — **GitHub Pages on this public repo**
  (free; a `deploy-lite` workflow runs `python3 tools/build_lite.py` and publishes
  `lite/`). Alternative — Cloudflare Pages, same build command, for anyone who forks
  and prefers it. State plainly that nothing personal is ever in the deployed bundle:
  progress lives only on the device, and every visitor gets the same static app.
- [ ] Verify: deploy it, open the live URL on an iPad, add to home screen, run a
  session, export a line, paste that literal line into `learners/shared/relay.md`, and
  confirm `/checkin` parses it. Paste the URL and the exported line in the PR.
- [ ] Commit `feat(lite): export, backup, and hosting`, PR.

---

## Self-review (v1.1, re-run 2026-08-11 against spec v1.1)

**Spec coverage.** §5 curriculum → Phase 1 (11 units, with 1.10 track-split).
§4 skills roster → Phase 2 (quiz/report/coach/checkin). §6 SRS → existing engine plus
the 6.3 parity test. §7 surfaces and accounts → Phase 4.2 (paid account provisioned
pre-delivery) and 4.3 (account-free Lite path). §8 webcam lab → Phase 3. §9 Handshake
Lite → Phase 6, all four sub-sections covered: generator (6.1), screens and learner
switcher (6.2), accessibility (Phase 6 non-negotiables), relay and hosting (6.4).
§3 content integrity → global constraints + every task's verify step, and restated as
a Phase 6 non-negotiable so the app inherits it.

**Risk coverage.** Every §10 row has an owner: hallucinated signs (global constraint),
fabricated URLs (verify + the SigningSavvy search caveat), **SRS drift (6.3, the row
added in v1.1)**, link rot (CI), stale relay (2.4's 14-day rule), motivation (unit
design), install friction (4.1), PII (global constraint).

**Type consistency.** Card types match `learners/README.md` across `/lesson`,
`/drill`, and `data.json`. The relay line format is specified once in
`learners/README.md` and referenced — not restated — by 2.4 and 6.4, so the producer
and consumer cannot drift. `get_landmarks`/`classify` stay consistent across 3.1→3.3.
`review(card, grade)` in 6.3 operates on the same field names as the TSV columns.

**Gaps deliberately left open.** A Lite-side learner's `profile.md` keeps `TUTOR_NAME_PENDING` until
their first launch relays real values — that is intended, not a placeholder. Unit 10's
two track tables are specified in the 1.10 row and the note beneath the table rather
than as separate tasks, because they are one file.

**No placeholders:** every task carries complete steps, exact commands, and the
evidence its PR must contain.
