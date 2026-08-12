#!/usr/bin/env bash
# Handshake bootstrap — power-on self-test.
# Run from the handshake/ directory:  bash install/bootstrap.sh
# Idempotent: safe to re-run any time. Works for both install paths:
#   clone   -> your .git already exists and tracks the public repo; updates via git pull
#   tarball -> no .git; we initialize a fresh local history (snapshot copy — updates
#              arrive as fresh tarballs, or adopt the clone path later)

set -euo pipefail
cd "$(dirname "$0")/.."

echo "== HANDSHAKE POWER-ON SELF-TEST"

fail=0
for tool in git python3 claude; do
  if command -v "$tool" >/dev/null 2>&1; then
    echo "   ok: $tool ($($tool --version 2>&1 | head -1))"
  else
    echo "   MISSING: $tool — see install/INSTALL.md Mission 01"
    fail=1
  fi
done
[ "$fail" -eq 1 ] && { echo "Toolchain incomplete. Fix the missing pieces, re-run."; exit 1; }

if [ -d .git ]; then
  echo "   ok: git history present (clone path — 'git pull' brings updates)"
  # Your learner data is yours: block accidental pushes to the public project.
  # Pulls still work. Undo (for maintainers only): git remote set-url --push origin <url>
  if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url --push origin no_push_configured_see_INSTALL_Mission_05
    echo "   ok: push disabled toward the public repo (pull-only; see Mission 05 for private backups)"
  fi
else
  echo "== Tarball path: initializing YOUR local git history"
  git init -b main -q
  git add -A
  git commit -q -m "unboxed: handshake payload received"
  echo "   ok: repository initialized, first commit made (snapshot copy — no remote)"
fi

echo "== Sanity check: expected structure"
for f in CLAUDE.md rules/tutor-rules.md curriculum/sources.md learners/_template/profile.md; do
  [ -f "$f" ] && echo "   ok: $f" || { echo "   MISSING: $f — payload incomplete"; exit 1; }
done

echo "== Verifying payload (lints lesson files + live-checks every lesson link)"
python3 tools/verify.py

echo
echo "== BOOTSTRAP COMPLETE"
echo "   Next: Mission 03. Run 'claude' and say: boot ceremony"
