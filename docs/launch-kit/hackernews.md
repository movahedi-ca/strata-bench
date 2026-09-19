# Show HN submission (copy-paste)

**Title:** Show HN: STRATA-Bench – a benchmark for whether AI agents know what a number is

**URL:** https://github.com/movahedi-ca/strata-bench

**Comment:**

Hi HN — STRATA-Bench is a 36-task benchmark for AI agents on fragmented
spatial-temporal market intelligence. The motivating observation: when six
frontier engines were asked for a five-year downtown condo rent series, they
split into Empirical Literalists (faithful to the board, honest about
geography), Synthetic Econometricians (modeled a downtown premium, disclosed
it), and Fragmented Extractors (OCR'd charts, skipped 9 of 20 quarters,
plotted the gaps as equal ticks).

The benchmark turns that into a scored protocol across six failure families
(geographic masking, temporal attrition, OCR laundering, silent interpolation,
non-uniform axes, source blending). The scoring idea we're proud of: agents
earn credit for disclose/tag/refuse/model — honesty is scorable — and hard
fails (geographic masking, silent interpolation, paywall fabrication) cap a
task at 55% of credit. There's a self-contained synthetic corpus so it runs
offline, three reference agents as regression fixtures, and a community
leaderboard where PRing your agent's run triggers an auto-scoring bot.

Try: `pip install strata-bench && strata-bench evaluate
submissions/examples/extractor.json --format text` — you'll watch the
extractor get caught.

Happy to discuss the failure taxonomy — especially whether "honesty is
scorable" generalizes beyond market intelligence.
