#!/usr/bin/env bash
# Package Handshake for delivery: one tarball, ready to email / USB / carrier pigeon.
#   bash tools/make_tarball.sh
# Output: dist/handshake-YYYYMMDD.tar.gz (from committed state — commit first).

set -euo pipefail
cd "$(dirname "$0")/.."

if ! git diff-index --quiet HEAD --; then
  echo "ERROR: uncommitted changes. Commit first — the tarball ships committed state only."
  exit 1
fi

mkdir -p dist
out="dist/handshake-$(date +%Y%m%d).tar.gz"
git archive --format=tar.gz --prefix=handshake/ -o "$out" HEAD
echo "Packaged: $out ($(du -h "$out" | cut -f1))"
echo "Recipient instructions: extract, then open install/INSTALL.md — Mission 00."
