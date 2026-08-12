# Source Allowlist

Every sign link in this system comes from the sites below. All URLs verified
2026-08-10 (`python3 tools/verify.py --links` re-checks continuously in CI).
**Link, never copy** — see `rules/tutor-rules.md` Rule 2.

## Primary teaching sources

| Source | URL | What it's for | Note |
|---|---|---|---|
| Lifeprint / ASL University | https://www.lifeprint.com/ | The backbone: free structured curriculum by Dr. Bill Vicars (Deaf professor, CSU Sacramento) | Lesson index: https://www.lifeprint.com/asl101/lessons/lessons.htm |
| Lifeprint fingerspelling | https://www.lifeprint.com/asl101/fingerspelling/fingerspelling.htm | Unit 01 core | |
| Bill Vicars on YouTube | https://www.youtube.com/billvicars | Full video lessons; pairs with Lifeprint pages | |
| ASL.ms | https://asl.ms/ | Fingerspelling receptive practice tool (adjustable speed) — also by Dr. Vicars | Core drill tool from unit 01 on |
| Handspeak | https://www.handspeak.com/ | ASL dictionary + culture articles, by a Deaf author | Word index: https://www.handspeak.com/word/ |
| SigningSavvy | https://www.signingsavvy.com/ | Video dictionary; predictable search URLs | Pattern: `https://www.signingsavvy.com/search/<word>` |
| StartASL | https://www.startasl.com/ | Alternative free structured course; second angle when a concept doesn't click | |

## Community & reference

| Source | URL | What it's for |
|---|---|---|
| National Association of the Deaf | https://www.nad.org/ | Community, advocacy, finding local resources (unit 11) |

## Engineering sources (webcam lab, Phase 3)

| Source | URL | What it's for |
|---|---|---|
| MediaPipe | https://ai.google.dev/edge/mediapipe/solutions/guide | Hand-landmark detection, local + free (Apache-2.0) |
| WLASL dataset | https://github.com/dxli94/WLASL | Research dataset, stretch goals only |
| Ollama | https://ollama.com/ | Phase 5 local-model stretch |

## Candidates — NOT yet on the allowlist

| Source | URL | Status |
|---|---|---|
| Gallaudet ASL Connect | https://gallaudet.edu/asl-connect/ | Site WAF blocks automated verification (403 to scripts). A human must load it in a browser and confirm before any link to it ships. |

## Adding a source

1. Human loads it in a browser; confirm it's free-to-access and reputable (prefer
   Deaf-created).
2. Add the row here with a verified date.
3. Only then may curriculum links use it. `verify.py` treats URLs whose host isn't in
   this file as errors.
