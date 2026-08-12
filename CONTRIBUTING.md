# Contributing to Handshake

Contributions are welcome — curriculum units, source vetting, Handshake Lite work,
and fixes of every size. Three things to know before your first PR.

## 1. The law

`rules/tutor-rules.md` governs everything, and Rule 1 is non-negotiable: **nothing
in this repository may describe how to produce a sign** — no handshape, movement,
or placement descriptions in hooks, hints, lesson prose, or code comments. Signs
are taught by linking to vetted sources; the text around a link addresses meaning
and context only. Rule 2 is its twin: **link, never copy** — no text, images, or
transcripts from source sites enter the repo. The educators behind them (most of
them Deaf) earn their living from their sites; send traffic, don't strip-mine it.

## 2. The gate

Every PR must pass:

```bash
python3 tools/verify.py
```

It lints unit format, learner-template schema, deck schema, checks every curriculum
URL against the allowlist and live reachability, and heuristically flags hook/hint
prose that looks like a production description (`NEEDS-HUMAN-EYES`). CI runs the
same command. Paste its output in your PR body — a claim of "passes" without the
output will not be merged. Note the flagger is a heuristic: a flagged hook isn't
automatically wrong, but it will be read by a human before merge, and a reworded
hook that doesn't trip it is usually the better hook anyway.

## 3. The boundaries

- **New sources** go through `curriculum/sources.md`'s admission process: a human
  loads the site in a browser, confirms it's free to access and reputable (prefer
  Deaf-created), and adds it with a verified date. PRs that link to hosts not on
  the allowlist fail verification. Search-style URLs (e.g.
  `signingsavvy.com/search/<word>`) return HTTP 200 even for words that don't
  exist — flag every one `NEEDS-HUMAN-EYES` in your PR body.
- **No personal data, ever.** This is a public repository. No real names, ages,
  health details, or family specifics of any learner — in files, issues, commit
  messages, or examples. Learner directories are created locally at install time
  and are not pushed here. Example names in docs are fictional.
- **Unit format** is specced in `curriculum/README.md` with
  `curriculum/unit-01-fingerspelling.md` as the reference implementation. The
  build plan (`docs/superpowers/plans/`) carries fully-specified task briefs —
  most open work is mirrored as a GitHub issue with acceptance criteria.

## Origin

Handshake was built inside one family, deliberately structured so the work could be
executed by inexpensive AI models against precise briefs with machine verification
and human review. The briefs and the delegation guide in `docs/` are part of the
project — improving *them* is as welcome as improving the code.
