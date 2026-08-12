# Handshake — ASL Tutor OS: Design Spec

**Date:** 2026-08-10 · **Status:** v1.2 (revised 2026-08-12)

> **v1.1:** second learner on a second surface (iPad web app), pairing model,
> per-learner tracks, relay. **v1.2:** repo restructured for public release — all
> learner personalization moved out of the repository into install-time templates;
> the two original learners appear below only as anonymous personas.

## 1. Who this is for

Handshake was built inside one family for a specific pair learning ASL together,
and is shared as open source because the pattern generalizes: adults who come to
sign language later in life — often because spoken conversation is getting harder
for someone they love — and the people learning alongside them. The two personas
that drove every design decision:

**The tinkerer.** A builder by training and temperament; needs a visual channel
for the conversations that matter. Historically resistant to "being helped,"
fully engaged by a system they get to assemble, inspect, and modify. For them,
the install *is* the first lesson and the exposed seams are the retention
mechanism.

**The appliance user.** Equally sharp — a practitioner's precision rather than a
builder's — but with zero interest in terminals, git, or configuration. Learning
so the two of them can talk. Wants to tap an icon and practice. For them, every
setup step is a defect, and there is no one sitting beside them when something
breaks.

Design consequences:

- **Two surfaces, one curriculum.** The full file-based system on a computer for
  the tinkerer; **Handshake Lite**, a zero-setup web app, for the appliance user.
  Same units, same scheduling algorithm, shared missions.
- **ASL is presented as a system.** Five parameters (handshape, movement, palm
  orientation, location, non-manual markers) encode the signal. Each learner's
  `background` profile line tells the tutor which world's metaphors to teach with.
- **Sessions are short.** 15–20 minutes daily beats 2 hours weekly. Streaks
  tracked and celebrated. No infantilizing tone, ever — dry humor yes,
  cheerleading no. Age is never treated as a limitation.
- **They learn as a pair.** Practising with a partner is the strongest retention
  mechanism available to an adult learner, and it means neither is doing this
  alone. One partner's encouragement becomes a designed feature, not a nag.

## 2. Goals and success criteria

**Goal 1 — working AI tutor.** A markdown + git + Claude Code system that runs
entirely on the learner's machine, teaches a 12-unit ASL curriculum, drills with
spaced repetition, and tracks progress in files the learner can read and hack.

**Goal 2 — an install the tinkerer runs solo.** Staged instructions
(`install/INSTALL.md`) as numbered missions with verification checkpoints,
engaging enough that setup itself keeps him hooked. Clone is the primary path;
a tarball snapshot exists for offline or ceremonial delivery.

**Goal 3 — an appliance for the partner.** The same curriculum as a tap-to-drill
web app: no account, no install beyond Add to Home Screen, no git. Also the
surface for testing with younger family members.

**Goal 4 (v1.2) — shareable.** The repository carries no personal data of any
real learner — names, ages, health details, and family specifics never appear in
files, commits, or issues. Learner directories are instantiated locally from
`learners/_template/` at install time and never pushed to the public repo.

Success looks like: the tinkerer completes the install solo; the daily habit
survives 3+ weeks for both; both fingerspell in both directions comfortably;
~100-sign core vocabulary by unit 8; and — the real measure — the pair holds a
conversation in ASL.

**Non-goals:** replacing human ASL instruction or Deaf community contact (the
curriculum points toward both); AI *generation* of sign videos or avatars; native
mobile apps; anything requiring a server or an account for the Lite surface.

## 3. The load-bearing rule: content integrity

LLMs cannot reliably describe how to produce a sign, and a wrong description
teaches wrong motor patterns that are expensive to unlearn. Therefore:

> **The tutor never invents or describes sign production from memory. Every sign
> is taught by linking to a vetted source on the allowlist**
> (`curriculum/sources.md`). The AI's job is sequencing, drilling, quizzing,
> scheduling, and encouragement — the *videos* teach the signs.

Enforcement layers, honestly labeled:

1. `rules/tutor-rules.md` — law for the runtime tutor (loaded via CLAUDE.md).
2. `curriculum/sources.md` — allowlist with verified-on dates and a
   human-in-the-browser admission process. Content is **linked, never copied**.
3. `tools/verify.py` — machine checks: URL allowlist + reachability (curriculum
   and decks), reachability of installer links, unit/template/deck schema lint,
   and a **heuristic** Rule-1 scan of hook/hint prose that flags
   production-description language as `NEEDS-HUMAN-EYES` (non-fatal — it feeds
   the human gate, it is not the enforcement). Runs in CI on every push/PR.
4. **The human gate is the enforcement of Rule 1 itself.** No machine check can
   prove a hook doesn't describe production; the maintainer's per-PR spot-check
   (`docs/delegation-guide.md`) is the layer that holds the rule, with layer 3
   surfacing candidates.

Search-URL caveat, learned the hard way and now law in three places: a dictionary
search URL returns HTTP 200 even for words the dictionary does not have. Status
proves the endpoint, not the item. Delegated workers flag constructed search URLs
`NEEDS-HUMAN-EYES`; the runtime tutor must confirm the sign is on the page with
the learner before adding a `lookup` card.

## 4. Architecture

Markdown-first, data on the learner's machine, git as source of truth. Layers:

| Layer | Path | Job |
|---|---|---|
| Entry | `CLAUDE.md`, `AGENTS.md` | Tutor persona + session protocol; tool-agnostic adapter |
| Law | `rules/tutor-rules.md` | No-invented-signs rule, session shape, tone, sourcing |
| Curriculum | `curriculum/` | 12 units + sources allowlist + unit format spec |
| Learners | `learners/<slug>/` | Per person: `profile.md`, `state.md`, `journal.md`, `deck.tsv` — created locally from `learners/_template/`, never shipped |
| Pair | `learners/shared/` | Two-person mission catalogue + relay log |
| Rituals | `.claude/skills/` | `/lesson`, `/drill` now; `/quiz`, `/report`, `/coach`, `/checkin` in Phase 2 |
| Lite | `lite/` | Handshake Lite: static web app built from the curriculum (Phase 6) |
| Tools | `tools/` | `verify.py`, `make_tarball.sh`, `build_lite.py` |
| Install | `install/` | `INSTALL.md` missions + `bootstrap.sh` (clone- and tarball-aware) |
| CI | `.github/workflows/verify.yml` | Runs `verify.py` on every push/PR |
| Community | `LICENSE` (MIT), `CONTRIBUTING.md` | Public-release layer |

Learner identity is machine-local: `learners/current.txt` (gitignored). The tutor
is **named by each learner** during the boot ceremony — small thing, large
ownership effect.

## 5. Curriculum

Twelve units, each a markdown file with frontmatter and six required sections:
**Why this unit** → **Watch** → **Learn** (sign, dictionary URL, meaning/context
hook) → **Drill** → **Family mission** → **Checkpoint**. Format spec with a
compliant worked example: `curriculum/README.md`.

00 Boot Ceremony · 01 The Alphabet Protocol (fingerspelling) · 02 First Contact ·
03 The Family Network · 04 Numbers & Time · 05 Daily Life · 06 Questions &
Grammar I (non-manual markers — video-taught only) · 07 Feelings & Health ·
08 Food & Restaurants · 09 Out & About · **10 Domain Vocabulary — track-split:**
a shared base plus `workshop` (tools, tech, making) and `clinical` (practice,
patients, care) extensions; `/lesson` teaches the base plus the learner's track ·
11 Deaf Culture & Community · 12 Conversation Ops.

Units 00–01 are the reference implementation; 02–12 are delegated Phase 1 tasks.
Each unit's solo mission is complemented by a two-person mission in
`learners/shared/missions.md`.

## 6. Practice engine (SRS)

`learners/<slug>/deck.tsv` — one row per card; columns and the SM-2-lite
algorithm are fully documented in `learners/README.md`, which is the **normative
spec** for both implementations. `/drill` selects ≤15 due cards, quizzes
(expressive against the source video; receptive fingerspelling via asl.ms),
rewrites rows, journals. Plain TSV on purpose. **Handshake Lite implements the
identical algorithm** over localStorage; `tools/test_srs_parity.py` (Phase 6)
asserts the two agree step-for-step.

## 7. Surfaces, accounts, and cost

| | Computer-side learner | Lite-side learner |
|---|---|---|
| Surface | Claude Code, full system | Handshake Lite web app |
| Account | Paid Claude plan | None (free Claude account optional, for chat only) |
| Progress | Files in git, live | On-device, relayed by one-line text export |
| Setup | Six install missions (the fun part) | Add to Home Screen |

**Why Lite can't be the Claude app's Code tab for a free-account learner:**
Claude Code has no iOS runtime — the mobile app is a client for cloud sessions
and Remote Control. Per the plan-availability matrix
(code.claude.com/docs/en/feature-availability), those features require a paid
plan (Pro/Max/Team); the Free column doesn't carry them. Remote Control would
additionally require someone else's computer to stay awake running the session.
For a free-account, zero-setup learner, a static web app is the option that
works; if that learner is ever upgraded, the Code tab against this same repo
becomes available with no data migration.

**Open/free components where they genuinely fit:** all sign content = free web
resources; webcam lab = MediaPipe Hands (Apache-2.0, local); SRS = plain code;
Lite = static HTML/JS, free hosting, zero inference cost. The expensive part
(LLM) does only what LLMs are good at. A fully-local Ollama path is a Phase 5
stretch investigation, not a requirement.

## 8. Webcam fingerspelling lab (Phase 3)

Python + MediaPipe Hands: recognizes the 24 static-handshape letters from a
webcam (J and Z involve motion — v1 detects and says so), drills "the machine
shows a word, you spell it back." Fully local, free, and genuinely fun to
calibrate — the tinker-bait layer. Calibration knobs deliberately exposed.

## 9. Handshake Lite (Phase 6)

A static, offline-capable web app — no framework, no build step beyond a
generator, no network calls except opening a source video.

- **Generated, not authored.** `tools/build_lite.py` parses the unit files and
  emits `lite/data.json`. One source of truth; the app cannot drift from the
  curriculum.
- **Screens:** Today (due cards) · Card (prompt → open the video → self-grade) ·
  Progress · Missions.
- **Learner switcher.** Multiple profiles per device in localStorage — one
  device can hold a primary learner or a handful of grandkids' test profiles
  without mixing data.
- **Accessibility is functional, not cosmetic:** base font ≥20px, tap targets
  ≥48px, WCAG AA contrast, no timed interactions, works in both orientations.
- **Relay:** Export emits one human-readable line to text to anyone; `/checkin`
  parses it (creating the learner from `_template/` on first sight). Backup
  emits full JSON, with a verified restore path.
- **Hosting:** the repo going public makes **GitHub Pages** the primary (free,
  no extra service); Cloudflare Pages is the documented alternative. Nothing
  personal is ever in the deployed bundle — progress lives on the device.

## 10. Risks

| Risk | Mitigation |
|---|---|
| LLM hallucinates sign descriptions | §3 layers: law + heuristic flagger + human gate |
| Delegated models fabricate URLs | verify.py in CI blocks merge; allowlist-only; search-URL caveat |
| Two SRS implementations drift | One normative spec (`learners/README.md`) + parity test (6.3) |
| Link rot | verify.py re-run on every push; installer links included |
| Relay is manual, so Lite-side state goes stale | `last_relay` tracked; stale = "unknown", never "stopped" (law in three files) |
| Motivation fade | 15-min sessions, streaks, partner missions, track-split unit 10, webcam lab as reward |
| Install friction kills adoption | Missions format, checkpoints, fresh-machine dry run gates delivery (4.1) |
| Personal data leaks into the public repo | Template model — learner dirs never ship; CONTRIBUTING bans it; commit/issue hygiene |
| Scope creep | Non-goals list; YAGNI enforced in plan |

## 11. Delegation strategy

Execution goes to less expensive models. The implementation plan
(`docs/superpowers/plans/2026-08-10-asl-tutor-buildout.md`) decomposes the phases
into self-contained briefs with exact files, complete schemas, acceptance
criteria, and the verification command each task must pass. GitHub issues mirror
the briefs. Review gates are the maintainer's: CI green plus a five-minute
spot-check per `docs/delegation-guide.md`.

**Sequencing decision (2026-08-11):** the computer-side learner ships first — that
system is nearly complete, and holding it for the Lite build would let new scope
delay the thing that's almost done. Phase 6 runs in parallel and lands after.
Personal delivery logistics (accounts, dates, who walks whom through what) live
in the maintainer's private planning system, not in this repo.
