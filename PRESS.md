# Press kit

## Boilerplate (100 words)

STRATA-Bench (Spatial-Temporal Retrieval, Alignment, Transparency & Audit)
is an open-source benchmark that evaluates whether AI agents can compile
longitudinal market intelligence from fragmented, geographically nested, and
temporally incomplete evidence. Across 36 sandbox tasks in six failure
families — geographic masking, temporal attrition, OCR laundering, silent
interpolation, non-uniform axes, and source blending — agents are scored on
whether they disclose, tag, refuse, or model uncertainty, not on whether they
produce a pretty dashboard. Born from a 2026 audit in which six frontier
engines split into Empirical Literalists, Synthetic Econometricians, and
Fragmented Extractors when asked for a five-year downtown rent series,
STRATA-Bench turns that failure mode into a scored protocol. Apache-2.0.

## Elevator pitch (30 words)

SWE-bench tests whether agents can patch code. STRATA-Bench tests whether
they know what a number is — scoring if AI agents hallucinate downtown
figures, silently fill missing quarters, or plot gaps as data.

## Fast facts

- 36 sandbox tasks + 3 live probes, 6 failure families (GEO/TEMP/SRC/INT/AXIS/SYN)
- Self-contained synthetic corpus: fictional Meridian Metro board, consultancy, listing site, adversarial traps
- Held-out gold; headline score = weighted blend of 6 dimensions; hard fails cap at 55%
- 3 reference agents shipped as regression fixtures (literalist / econometrician / extractor)
- License: Apache-2.0 · Python 3.10+ · `pip install strata-bench`
- Community leaderboard: PR your agent's run, get auto-scored

## Key messages

1. Agents fail in *structured* ways — STRATA-Bench names and scores each one.
2. Honesty is scorable: disclose, tag, refuse, or model beats silent fabrication.
3. The unconstrained prompt "give me downtown rents over five years" is a trap; the benchmark teaches the protocol-compliant brief.

## Links

- Repo: https://github.com/movahedi-ca/strata-bench
- Docs: https://movahedi-ca.github.io/strata-bench/
- Announcement: https://github.com/movahedi-ca/strata-bench/discussions/6
- Release: https://github.com/movahedi-ca/strata-bench/releases/tag/v1.1.0
- Citation: CITATION.cff (BibTeX in README)

## Media

- Hero image: `docs/assets/hero.png` (1600×686, dark strata/lens illustration)
- Social card: `docs/assets/social-card.png`
- Promo clip: `docs/assets/promo.mp4`

Free to use with attribution to the STRATA-Bench project.

## Suggested headlines

- "New benchmark catches AI agents hallucinating downtown real-estate data"
- "STRATA-Bench: the test that asks whether AI knows what a number is"
- "36 ways AI agents fudge market data — now a scored benchmark"

## Contact

Maintainer: Mohammad Movahedi — via GitHub Issues:
https://github.com/movahedi-ca/strata-bench/issues
