# r/MachineLearning post (copy-paste)

**Title:** [P] STRATA-Bench: a 36-task benchmark for whether AI agents know what a number is

**Body:**

**TL;DR:** New open-source benchmark (Apache-2.0) scoring whether AI agents can compile longitudinal market intelligence from fragmented, geographically nested, temporally incomplete evidence — without relabeling metro figures as downtown, silently interpolating missing quarters, or plotting gaps as data.

**Motivation:** A 2026 audit asked six frontier engines for a five-year downtown condo rent series from public sources. They split into three archetypes: Empirical Literalists (faithful to the board, honest about geography), Synthetic Econometricians (modeled a downtown premium, disclosed it), and Fragmented Extractors (OCR'd charts, skipped 9/20 quarters, plotted gaps as equal ticks). This benchmark turns that failure mode into a scored protocol.

**What's in it:**
- 36 sandbox tasks + 3 live probes across 6 failure families: GEO (geographic masking), TEMP (temporal attrition), SRC (source blending/OCR), INT (silent interpolation), AXIS (non-uniform axes), SYN (synthetic blending)
- Self-contained synthetic corpus (fictional Meridian Metro board, consultancy, listing site, adversarial traps) — no external data needed
- Scoring: disclose / tag / refuse / model — hard fails (geographic masking, silent interpolation, paywall fabrication) cap a task at 55% of earned credit
- 3 reference agents shipped as regression fixtures

**Try it:** `pip install strata-bench`, then `strata-bench evaluate submissions/examples/extractor.json --format text` — watch the reference extractor get caught.

**New in v1.1.0:** community leaderboard — PR your agent's run under `submissions/community/` and a bot auto-scores it and posts a scorecard.

Repo: github.com/movahedi-ca/strata-bench · Docs: movahedi-ca.github.io/strata-bench

Happy to answer questions about the failure taxonomy and scoring protocol.
