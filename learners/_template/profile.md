# Profile — TEMPLATE (copy this whole directory to `learners/<your-slug>/`)

- learner: SLUG_PENDING
- display_name: NAME_PENDING
- tutor_name: TUTOR_NAME_PENDING
- goal: GOAL_PENDING
- surface: claude-code
- track: workshop
- partner: none
- background: BACKGROUND_PENDING

Field notes:

- `learner` — short lowercase slug, must match the directory name.
- `tutor_name` and `goal` are set during the Boot Ceremony
  (`curriculum/unit-00-boot-ceremony.md`); leave the placeholders until then — a
  `TUTOR_NAME_PENDING` value is how the tutor knows to run the ceremony.
- `surface` — `claude-code` (the full system, on a computer) or `lite` (the
  Handshake Lite web app; such a learner's files here are relayed snapshots, not
  live state — see `learners/README.md`).
- `track` — which vocabulary variant track-split units teach you: `workshop`
  (tools, tech, making things) or `clinical` (practice, patients, care). Pick
  whichever is closer to your world; you can hack in your own track later
  (`tools/verify.py` holds the enum).
- `partner` — another learner's slug, or `none`. Partners see each other's streak
  and unit position and share the missions in `learners/shared/missions.md`.
  Journals stay private either way.
- `background` — one line about the world you come from ("thirty years of
  air-traffic control", "taught high-school chemistry"). The tutor reads it and
  teaches to it.
