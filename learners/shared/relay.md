# Relay — progress lines pasted in from Handshake Lite

Handshake Lite's **Export** button produces one line of plain text. Paste those
lines here, newest at the bottom, exactly as received. `/checkin` reads the last
line per learner and updates their `state.md` — creating `learners/<slug>/` from
`_template/` the first time a new name appears.

Expected format:

```
Handshake · <name> · day <streak> · unit <n> · <total> cards (<due> due) · asl.ms speed <n> · nemeses: A, B, C · <YYYY-MM-DD>
```

Paste lines verbatim even if a field is missing or the format drifts — a
partially-parseable real line beats a tidied-up guess. `/checkin` reports what it
couldn't read rather than filling it in.

## Lines

*(none yet)*
