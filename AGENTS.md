# Handshake — Agent Entry Point (tool-agnostic)

Any AI coding tool working in this repo: read `CLAUDE.md` for the tutor persona and
session protocol, and `rules/tutor-rules.md` for the law. The one non-negotiable,
restated here because it matters most:

**Never describe how to produce an ASL sign from model memory.** Signs are taught only
by linking to sources on the allowlist in `curriculum/sources.md`. Constructed URLs
must be verified (`python3 tools/verify.py --links`) before they ship.

For project/build work (as opposed to tutoring sessions): the plan is
`docs/superpowers/plans/2026-08-10-asl-tutor-buildout.md`; every task's acceptance
criteria include a passing `python3 tools/verify.py`.
