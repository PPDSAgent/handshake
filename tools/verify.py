#!/usr/bin/env python3
"""Handshake verifier: link checks, unit lint, deck lint.

Usage:
    python3 tools/verify.py            # run everything
    python3 tools/verify.py --links    # URL allowlist + reachability only
    python3 tools/verify.py --units    # curriculum format lint only
    python3 tools/verify.py --index    # units-index.md vs frontmatter consistency
    python3 tools/verify.py --deck     # deck.tsv schema lint, all learners
    python3 tools/verify.py --learners # template + learner profile/state lint
    python3 tools/verify.py --missions # partner missions vs what each unit teaches
    python3 tools/verify.py --hooks    # Rule-1 heuristic on hook/hint prose
    python3 tools/verify.py --hygiene  # public-repo personal-data heuristic, all tracked files

Exit 0 = clean. Exit 1 = findings (printed). Stdlib only — no installs needed.
"""

import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "curriculum" / "sources.md"
LEARNERS = ROOT / "learners"
PROFILE_KEYS = ["learner", "display_name", "tutor_name", "goal", "surface", "track",
                "partner", "background"]
STATE_KEYS = ["current_unit", "streak", "last_session", "asl_ms_speed"]
SURFACES = {"claude-code", "lite"}
TRACKS = {"workshop", "clinical"}
NON_LEARNER_DIRS = {"shared", "_template"}
# Heuristic flag for sign-production language in hooks/hints (Rule 1). Non-fatal:
# a match means NEEDS-HUMAN-EYES, not automatically wrong.
PRODUCTION_RE = re.compile(
    r"(?i)\b(handshapes?|palms?|fingers?|thumbs?|wrists?|knuckles?|fists?|chin|"
    r"forehead|cheeks?|chest|shoulders?|moves?|moving|motion|movement|circles?|"
    r"taps?|twists?|salutes?|flat hand|index finger)\b")

warnings = []


def warn(msg):
    warnings.append(msg)
    print(f"  NEEDS-HUMAN-EYES  {msg}")


def decks():
    """Every real learner's deck: [(slug, Path), ...]. Excludes the template."""
    return sorted((d.name, d / "deck.tsv") for d in LEARNERS.iterdir()
                  if d.is_dir() and d.name not in NON_LEARNER_DIRS
                  and (d / "deck.tsv").exists())
UA = {"User-Agent": "Mozilla/5.0 (Handshake verify.py; personal ASL tutor link check)"}
URL_RE = re.compile(r"https?://[^\s)\]|<>`\"']+")
DECK_COLS = ["id", "type", "prompt", "answer_hint", "source_url", "unit", "ease",
             "interval_days", "due", "reps", "lapses", "added"]
CARD_TYPES = {"fingerspell", "vocab", "phrase", "lookup"}
UNIT_SECTIONS = ["## Why this unit", "## Watch", "## Learn", "## Drill",
                 "## Family mission", "## Checkpoint"]

errors = []


def err(msg):
    errors.append(msg)
    print(f"  FAIL  {msg}")


def trim(u):
    """Strip trailing sentence punctuation. A URL written mid-prose is routinely
    followed by ; : . , or a closing paren — none of which is part of the link."""
    return u.rstrip(".,;:!?")


def host_of(url):
    h = url.split("/")[2].lower()
    return h[4:] if h.startswith("www.") else h


def allowed_hosts():
    """Hosts from sources.md, excluding tables under a 'Candidates' heading."""
    hosts = set()
    section_ok = True
    for line in SOURCES.read_text().splitlines():
        if line.startswith("## "):
            section_ok = "candidate" not in line.lower()
        if section_ok:
            for u in URL_RE.findall(line):
                hosts.add(host_of(u))
    return hosts


def reachable(url):
    for _ in range(2):  # one retry — external sites hiccup
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status < 400:
                    return True
        except Exception:
            continue
    return False


def check_links():
    print("== links")
    hosts = allowed_hosts()
    urls = set()
    for md in (ROOT / "curriculum").glob("*.md"):
        if md.name == "sources.md":
            continue  # sources.md is the allowlist itself, checked below
        for u in URL_RE.findall(md.read_text()):
            urls.add((trim(u), md.name))
    for slug, deck in decks():
        for row in deck.read_text().splitlines()[1:]:
            cells = row.split("\t")
            if len(cells) == len(DECK_COLS) and cells[4].startswith("http"):
                urls.add((cells[4], f"{slug}/deck.tsv"))
    # allowlist itself must be reachable too (skip the Candidates section)
    section_ok = True
    for line in SOURCES.read_text().splitlines():
        if line.startswith("## "):
            section_ok = "candidate" not in line.lower()
        if section_ok:
            for u in URL_RE.findall(line):
                urls.add((trim(u), "sources.md"))
    for url, origin in sorted(urls):
        if host_of(url) not in hosts:
            err(f"{origin}: host not on allowlist -> {url}")
        elif not reachable(url):
            err(f"{origin}: unreachable -> {url}")
    # Installer + README links: reachability only (no allowlist — they point at
    # toolchain sites, not sign sources). Self-references to this repo are
    # skipped: they 404 to anonymous checks while the repo is private.
    reach_only = set()
    for md in [ROOT / "README.md", *(ROOT / "install").glob("*.md")]:
        for u in URL_RE.findall(md.read_text()):
            u = trim(u)
            if "github.com/PPDSAgent/handshake" in u:
                continue
            reach_only.add((u, md.name))
    for url, origin in sorted(reach_only):
        if not reachable(url):
            err(f"{origin}: unreachable -> {url}")
    print(f"  checked {len(urls)} curriculum urls + {len(reach_only)} installer urls")


def check_units():
    print("== units")
    for md in sorted((ROOT / "curriculum").glob("unit-*.md")):
        text = md.read_text()
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not m:
            err(f"{md.name}: missing frontmatter")
            continue
        fm = m.group(1)
        for field in ("unit:", "title:", "status:", "est_sessions:"):
            if field not in fm:
                err(f"{md.name}: frontmatter missing '{field}'")
        status = re.search(r"status:\s*(\S+)", fm)
        if status and status.group(1) not in ("draft", "built", "reviewed"):
            err(f"{md.name}: bad status '{status.group(1)}'")
        pos = 0
        for section in UNIT_SECTIONS:
            found = text.find(section, pos)
            if found == -1:
                err(f"{md.name}: section missing or out of order: '{section}'")
            else:
                pos = found
        for line in text.splitlines():
            if line.startswith("|") and "http" in line and line.count("|") not in (0, 4):
                err(f"{md.name}: Learn table row needs exactly 3 columns: {line[:60]}")


def check_deck():
    print("== decks")
    total = 0
    for slug, deck in decks():
        where = f"{slug}/deck.tsv"
        lines = deck.read_text().splitlines()
        if not lines or lines[0].split("\t") != DECK_COLS:
            err(f"{where}: header row does not match spec (see learners/README.md)")
            continue
        seen = set()
        for n, row in enumerate(lines[1:], start=2):
            cells = row.split("\t")
            if len(cells) != len(DECK_COLS):
                err(f"{where} line {n}: {len(cells)} columns, expected {len(DECK_COLS)}")
                continue
            cid, ctype, ease, due, added = cells[0], cells[1], cells[6], cells[8], cells[11]
            if cid in seen:
                err(f"{where} line {n}: duplicate id '{cid}'")
            seen.add(cid)
            if ctype not in CARD_TYPES:
                err(f"{where} line {n}: bad type '{ctype}'")
            try:
                e = float(ease)
                if not 1.3 <= e <= 2.8:
                    err(f"{where} line {n}: ease {e} outside [1.3, 2.8]")
            except ValueError:
                err(f"{where} line {n}: ease not a number")
            for label, val in (("due", due), ("added", added)):
                try:
                    date.fromisoformat(val)
                except ValueError:
                    err(f"{where} line {n}: {label} not ISO date: '{val}'")
        total += len(lines) - 1
    print(f"  checked {total} cards across {len(decks())} learners")


def check_learners():
    print("== learners")
    errors_before = len(errors)
    # The template must exist and carry every key — it is what installs copy.
    tmpl = LEARNERS / "_template"
    for fname, keys in (("profile.md", PROFILE_KEYS), ("state.md", STATE_KEYS)):
        f = tmpl / fname
        if not f.exists():
            err(f"_template/{fname}: missing — installs copy this directory")
            continue
        text = f.read_text()
        for key in keys:
            if not re.search(rf"(?m)^-\s+{re.escape(key)}:", text):
                err(f"_template/{fname}: missing key '{key}'")
    for fname in ("journal.md", "deck.tsv"):
        if not (tmpl / fname).exists():
            err(f"_template/{fname}: missing — installs copy this directory")
    template_clean = len(errors) == errors_before
    # Real learners are created locally at install time; zero is normal for a
    # fresh clone (and required for the public repo — no personal data ships).
    slugs = [s for s, _ in decks()]
    for slug in slugs:
        d = LEARNERS / slug
        for fname, keys in (("profile.md", PROFILE_KEYS), ("state.md", STATE_KEYS)):
            f = d / fname
            if not f.exists():
                err(f"{slug}/{fname}: missing")
                continue
            text = f.read_text()
            for key in keys:
                if not re.search(rf"(?m)^-\s+{re.escape(key)}:", text):
                    err(f"{slug}/{fname}: missing key '{key}'")
        prof = (d / "profile.md")
        if prof.exists():
            text = prof.read_text()
            got = re.search(r"(?m)^-\s+learner:\s*(\S+)", text)
            if got and got.group(1) != slug:
                err(f"{slug}/profile.md: learner '{got.group(1)}' != directory '{slug}'")
            for key, valid in (("surface", SURFACES), ("track", TRACKS)):
                m = re.search(rf"(?m)^-\s+{key}:\s*(\S+)", text)
                if m and m.group(1) not in valid:
                    err(f"{slug}/profile.md: {key} '{m.group(1)}' not in {sorted(valid)}")
            partner = re.search(r"(?m)^-\s+partner:\s*(\S+)", text)
            if partner and partner.group(1) not in slugs + ["none"]:
                err(f"{slug}/profile.md: partner '{partner.group(1)}' is not a learner")
        if not (d / "journal.md").exists():
            err(f"{slug}/journal.md: missing")
    who = ", ".join(slugs) if slugs else "none (fresh copy — created at install)"
    tmpl_word = "template ok" if template_clean else "template FAILING"
    print(f"  {tmpl_word}; {len(slugs)} local learner(s): {who}")


def check_index():
    """units-index.md is authoritative; frontmatter must agree with it.

    Added after the Phase 1 batch shipped 11 units whose frontmatter said `built`
    while the index still said `planned` — a contradiction nothing checked.
    """
    print("== index")
    idx = ROOT / "curriculum" / "units-index.md"
    rows = {}
    for line in idx.read_text().splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|", line)
        if m:
            rows[int(m.group(1))] = {"file": m.group(2), "title": m.group(3),
                                     "status": m.group(4), "est": int(m.group(5))}
    files = sorted((ROOT / "curriculum").glob("unit-*.md"))
    seen = set()
    for f in files:
        text = f.read_text()
        fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not fm:
            continue  # check_units already reports missing frontmatter
        def field(k):
            m = re.search(rf"(?m)^{k}:\s*(.+?)\s*$", fm.group(1))
            return m.group(1) if m else None
        num = field("unit")
        try:
            num = int(num)
        except (TypeError, ValueError):
            err(f"{f.name}: frontmatter 'unit:' is not an integer")
            continue
        seen.add(num)
        # the filename encodes the unit number too — they must agree
        fnum = re.match(r"unit-(\d+)-", f.name)
        if fnum and int(fnum.group(1)) != num:
            err(f"{f.name}: frontmatter unit {num} != filename unit {int(fnum.group(1))}")
        row = rows.get(num)
        if not row:
            err(f"{f.name}: unit {num} is not listed in units-index.md")
            continue
        if row["file"] != f.name:
            err(f"units-index.md row {num:02d}: filename '{row['file']}' != actual '{f.name}'")
        for label, got, want in (("title", field("title"), row["title"]),
                                 ("status", field("status"), row["status"]),
                                 ("est_sessions", field("est_sessions"), str(row["est"]))):
            if got != want:
                err(f"{f.name}: {label} '{got}' != units-index.md '{want}'")
    for num, row in rows.items():
        if num not in seen:
            err(f"units-index.md lists unit {num:02d} ({row['file']}) but no such file exists")
    # A stated total that a machine does not add is a total that goes stale — it did.
    total = sum(r["est"] for r in rows.values())
    stated = re.search(r"\*\*Total:\s*(\d+)\s*sessions\*\*", idx.read_text())
    if not stated:
        err("units-index.md: no '**Total: N sessions**' line to check the column against")
    elif int(stated.group(1)) != total:
        err(f"units-index.md: states {stated.group(1)} total sessions, column sums to {total}")
    print(f"  checked {len(files)} unit files against {len(rows)} index rows; "
          f"est_sessions column sums to {total}")


def taught_by_unit():
    """Cumulative ALL-CAPS glosses taught at or before each unit number."""
    cum, out = set(), {}
    for n in range(0, 100):
        for f in (ROOT / "curriculum").glob(f"unit-{n:02d}-*.md"):
            learn = re.search(r"## Learn\n(.*?)(?=\n## )", f.read_text(), re.S)
            if learn:
                for line in learn.group(1).splitlines():
                    if line.startswith("|") and "http" in line:
                        gloss = line.split("|")[1].strip()
                        cum.update(re.findall(r"[A-Z][A-Z\-']{1,}", gloss))
        out[n] = set(cum)
    return out


def check_missions():
    """Partner missions must not use a gloss before its unit teaches it, and any
    count they name must match that unit's Learn table.

    Added after the missions file — written before the curriculum existed — drifted
    twice: it drilled a sign that had moved to a later unit, and named a count the
    track tables no longer matched."""
    print("== missions")
    f = LEARNERS / "shared" / "missions.md"
    if not f.exists():
        err("learners/shared/missions.md: missing")
        return
    taught = taught_by_unit()
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
    rows = 0
    for line in f.read_text().splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|", line)
        if not m:
            continue
        unit, text = int(m.group(1)), m.group(2)
        rows += 1
        for g in sorted(set(re.findall(r"\b[A-Z][A-Z\-]{2,}\b", text)) - {"ASL"}):
            if g not in taught.get(unit, set()):
                warn(f"missions.md unit {unit:02d}: gloss '{g}' is not taught by "
                     f"unit {unit:02d} or earlier")
        uf = list((ROOT / "curriculum").glob(f"unit-{unit:02d}-*.md"))
        if uf:
            body = uf[0].read_text()
            learn = re.search(r"## Learn\n(.*?)(?=\n## )", body, re.S)
            block = learn.group(1) if learn else ""
            rows_all = [l for l in block.splitlines() if l.startswith("|") and "http" in l]
            # A track-split unit has several legitimate counts: the whole table, the
            # shared base, or one track. Accept any of them.
            valid = {len(rows_all)}
            segs = re.split(r"\n###\s+Track:", block)
            if len(segs) > 1:
                valid.add(len([l for l in segs[0].splitlines()
                               if l.startswith("|") and "http" in l]))
                for s in segs[1:]:
                    valid.add(len([l for l in s.splitlines()
                                   if l.startswith("|") and "http" in l]))
            for w, v in words.items():
                if re.search(rf"\b{w}\b signs?\b", text) and v not in valid:
                    warn(f"missions.md unit {unit:02d}: says '{w} signs' but the unit's "
                         f"Learn table offers {sorted(valid)}")
    print(f"  checked {rows} mission rows")


def check_public_hygiene():
    """This is a public repo: no personal data of any real learner, anywhere.
    The governing files promise it; this scan looks for it. Every tracked file,
    no extension filter. Non-fatal — flags mean a human reads them."""
    print("== public hygiene")
    import subprocess
    age_re = re.compile(r"(?i)\b[6-9][0-9][- ]?(?:year|yr)|\bin (?:their|his|her) "
                        r"(?:sixties|seventies|eighties|nineties)\b")
    rel_re = re.compile(r"(?i)\b(?:dad|mom|father|mother)\b|\bmy (?:wife|husband|parents)\b")
    health_re = re.compile(r"(?i)losing (?:their|his|her) hearing|\bdiagnos|\bhearing loss\b")
    try:
        tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                                 cwd=ROOT, timeout=10).stdout.splitlines()
    except Exception as e:
        err(f"public-hygiene: could not list tracked files ({e})")
        return
    n = 0
    for rel in tracked:
        if rel == "tools/verify.py":
            continue  # the scanner's own pattern definitions are not personal data
        p = ROOT / rel
        try:
            text = p.read_text()
        except Exception:
            continue  # binary or unreadable — nothing to scan
        n += 1
        for lineno, line in enumerate(text.splitlines(), start=1):
            for label, rx in (("age", age_re), ("relationship", rel_re),
                              ("health", health_re)):
                m = rx.search(line)
                # ALL-CAPS matches are ASL glosses (MOTHER, FATHER…), not people.
                if m and not m.group(0).isupper():
                    warn(f"{rel}:{lineno}: {label} phrase ('{m.group(0)}'): "
                         f"{line.strip()[:60]}")
    print(f"  scanned {n} tracked files")


def check_hooks():
    """Heuristic Rule-1 lint: flag production-description language in Learn-table
    hooks and deck answer_hints. Non-fatal — flags mean a human reads them."""
    print("== hooks (Rule 1 heuristic)")
    n = 0
    for md in sorted((ROOT / "curriculum").glob("unit-*.md")):
        for line in md.read_text().splitlines():
            if line.startswith("|") and "http" in line:
                cells = line.split("|")
                if len(cells) >= 4:
                    hook = cells[3]
                    m = PRODUCTION_RE.search(hook)
                    if m:
                        warn(f"{md.name}: hook may describe production "
                             f"('{m.group(0)}'): {hook.strip()[:60]}")
                    n += 1
    for slug, deck in decks():
        for row in deck.read_text().splitlines()[1:]:
            cells = row.split("\t")
            if len(cells) == len(DECK_COLS):
                m = PRODUCTION_RE.search(cells[3])
                if m:
                    warn(f"{slug}/deck.tsv: answer_hint may describe production "
                         f"('{m.group(0)}'): {cells[3][:60]}")
                n += 1
    # Rule 1 applies to ALL unit prose, not just hooks — the Why/Watch/Drill/
    # Mission/Checkpoint sections can describe production just as easily.
    prose = 0
    for md in sorted((ROOT / "curriculum").glob("unit-*.md")):
        for lineno, line in enumerate(md.read_text().splitlines(), start=1):
            s = line.strip()
            if not s or s.startswith("|") or s.startswith("#") or s.startswith("---"):
                continue  # tables handled above; headings and frontmatter carry no hooks
            prose += 1
            m = PRODUCTION_RE.search(s)
            if m:
                warn(f"{md.name}:{lineno}: prose may describe production "
                     f"('{m.group(0)}'): {s[:70]}")
    # Multi-gloss phrase cards must cite where the ORDER came from. ASL word order is
    # not this repo's to invent — a card naming two or more glosses without a URL in
    # the same bullet is Rule 1 at the phrase level.
    for md in sorted((ROOT / "curriculum").glob("unit-*.md")):
        drill = re.search(r"## Drill\n(.*?)(?=\n## )", md.read_text(), re.S)
        if not drill:
            continue
        for bullet in re.split(r"\n(?=\s*-\s)", drill.group(1)):
            # Two acceptable answers: cite where the order is attested, or say plainly
            # that it is a drill sequence and not a sentence.
            disclaimed = re.search(r"(?i)fluency drill|not (an )?attested sentence|"
                                   r"not attested|drill sequence", bullet)
            for prompt in re.findall(r'"Sign:\s*([^"]+)"', bullet):
                glosses = re.findall(r"\b[A-Z][A-Z\-']{1,}\b", prompt)
                if len(glosses) >= 2 and "http" not in bullet and not disclaimed:
                    warn(f"{md.name}: phrase card \"{' '.join(prompt.split())}\" names "
                         f"{len(glosses)} glosses but its bullet neither cites a URL "
                         f"nor calls itself a fluency drill — ASL word order is not "
                         f"this repo's to invent")

    # Sign count is a guideline (8-15), not law — units 00/01/10/11 are legitimately
    # outside it. Surface, never fail.
    for md in sorted((ROOT / "curriculum").glob("unit-*.md")):
        body = md.read_text()
        learn = re.search(r"## Learn\n(.*?)(?=\n## )", body, re.S)
        if learn:
            count = len([l for l in learn.group(1).splitlines()
                         if l.startswith("|") and "http" in l])
            # Suppress where the unit's own prose already owns the deviation — a
            # guideline the author consciously departed from and explained is not a
            # finding, and a noisy gate is one people stop reading.
            explained = re.search(r"(?i)above the usual 8[–-]15|below the usual 8[–-]15|"
                                  r"deliberately small|track-split design|"
                                  r"not an oversight|on purpose", body)
            if count and not 8 <= count <= 15 and not explained:
                warn(f"{md.name}: {count} signs in ## Learn (guideline is 8-15) — "
                     f"rebalance, or explain the deviation in the unit's own prose")
    print(f"  scanned {n} hooks/hints and {prose} prose lines")


if __name__ == "__main__":
    args = sys.argv[1:]
    run_all = not args
    if run_all or "--units" in args:
        check_units()
    if run_all or "--index" in args:
        check_index()
    if run_all or "--learners" in args:
        check_learners()
    if run_all or "--missions" in args:
        check_missions()
    if run_all or "--deck" in args:
        check_deck()
    if run_all or "--hooks" in args:
        check_hooks()
    if run_all or "--hygiene" in args:
        check_public_hygiene()
    if run_all or "--links" in args:
        check_links()
    summary = f"{len(warnings)} NEEDS-HUMAN-EYES flag(s) for review" if warnings \
        else "0 flags"
    if errors:
        print(f"\n{len(errors)} finding(s), {summary}. Fix before shipping — Rule 3.")
        sys.exit(1)
    print(f"\nAll clean ({summary}).")
