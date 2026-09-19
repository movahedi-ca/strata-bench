# LinkedIn post (copy-paste)

Most AI agent benchmarks test whether an agent can complete a task. We built one that tests whether an agent knows what a number is.

STRATA-Bench (Spatial-Temporal Retrieval, Alignment, Transparency & Audit) is a new open-source benchmark for AI agents on fragmented spatial-temporal market intelligence. It grew out of a 2026 audit where six frontier engines were asked for a five-year downtown condo rent series — and split into three archetypes: Empirical Literalists (faithful to the public board, honest about geography), Synthetic Econometricians (modeled a downtown premium and disclosed it), and Fragmented Extractors (OCR'd charts, skipped nine of twenty quarters, plotted the gaps as equal ticks).

The benchmark turns that failure mode into a scored protocol:
• 36 sandbox tasks across 6 failure families — geographic masking, temporal attrition, OCR laundering, silent interpolation, non-uniform axes, source blending
• Scored on whether agents disclose, tag, refuse, or model uncertainty — not on dashboard aesthetics
• Hard fails (geographic masking, silent interpolation, paywall fabrication…) cap a task at 55% of credit

v1.1.0 launched today with a community leaderboard — PR your agent's run and a bot scores it automatically.

For teams building research agents, data analysts, or anything that compiles longitudinal intelligence from fragmented evidence: this is the test that checks whether your pipeline is honest about its gaps.

Repo: github.com/movahedi-ca/strata-bench
Docs: movahedi-ca.github.io/strata-bench

#AI #LLM #Benchmark #AIAgents #OpenSource #DataScience
