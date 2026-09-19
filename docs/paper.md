# STRATA-Bench: Evaluating AI Agents on Fragmented Spatial-Temporal Market Intelligence

**Mohammad Movahedi**  
The Globe and Mail / Northeastern University  
[movahedi.ca](https://movahedi.ca) · [github.com/movahedi-ca/strata-bench](https://github.com/movahedi-ca/strata-bench)

Technical report, v1.0.0 · September 2026

## Abstract

Frontier agents are routinely asked to produce multi-year regional market retrospectives. We show that this task is not a retrieval problem but an *integrity* problem. Public statistical systems almost always publish a coarse geography on a complete cadence and a fine geography behind a paywall or on a sparser, differently unitised series. In a motivating audit of six frontier engines on a five-year condominium rental brief, models clustered into three archetypes: empirical literalists, who kept the public board and named the mismatch; synthetic econometricians, who built a downtown premium and said so; and fragmented extractors, who read charts, skipped nine of twenty quarters, and plotted those holes as equal ticks.

STRATA-Bench operationalises those failure modes. Track Sandbox is a 36-task, self-contained corpus over a fictional metro whose cycle shape matches 2021–2026 North American rental markets. Gold is held out. The harness scores six dimensions (temporal coverage, source grounding, spatial precision, statistical rigor, visual/axis integrity, macro narrative) and applies hard-fail multipliers for geographic masking, silent interpolation, categorical axes on gappy series, OCR laundering, paywall fabrication, unit collapse, and 2026 truncation. Literalism is not privileged over modeling; **disclosure** is.

## 1. Introduction

Agent benchmarks have matured along two axes: *can the system change a repository so tests pass* (SWE-bench) and *can it chain tools to answer a question a human finds easy* (GAIA). A third axis is largely unmeasured: **does the system know the referent of a number**.

Institutional research briefs are specified in colloquial geography (“downtown”, “the city”, “the region”) and answered in administrative geography (board-wide metro, municipal districts, census metropolitan areas). The two rarely coincide. When they do not, a capable-looking agent has four honest moves — refuse, disclose and substitute, disclose and model, disclose and leave gaps — and a large space of dishonest ones: relabel, splice, interpolate silently, read pixels off a chart, average incompatible sources.

We treat those dishonest moves as first-class errors with named codes, not as “the model was slightly off.”

## 2. Motivating audit

A 2026 comparative evaluation asked six frontier engines for a quarterly condominium rental retrospective covering Q3 2021 through Q2/Q3 2026, with the user focused on downtown Toronto. Authoritative public files (TRREB) cover the GTA; C01/C08 district tables are subscriber-only; Urbanation-class consultancies publish $/psf on an irregular cadence.

Observed behaviours, later encoded as STRATA families:

1. **Geographic masking.** Public GTA figures emitted under a downtown label, or downtown requested and GTA delivered without a disclaimer.
2. **OCR / visual extraction.** Rounded numbers admitted to be “read off graphics,” missing nine quarters.
3. **Non-uniform temporal axis.** Eleven recovered quarters plotted as equal categorical ticks, so an 18-month hole had the visual width of one quarter.
4. **Interpolation opacity.** Missing points dropped, filled, or invented with no marker convention.
5. **Premature truncation.** Series ending in 2025, missing the 2026 trough and first rebound.

The audit is the *motivation*, not the benchmark. STRATA-Bench does not redistribute third-party tables. It rebuilds the *structure* of the problem in a synthetic metro.

## 3. Design

**Meridian Metro** publishes 20 consecutive quarterly 1-bed and 2-bed asking rents (MREB public). Core districts C-1 and C-8 are paywalled at the board; UrbanPulse publishes a core $/psf monitor on Q1/Q3 (plus two Q4s). LeaseWatch publishes rounded, geographically ambiguous 1-bed snapshots with a seven-quarter hole and a 2026 cutoff. Trap files state the paywall and exhibit a deliberately broken ASCII chart.

Gold core = metro × 1.115, nearest dollar. Peak 2023-Q3, trough 2026-Q1, first rebound 2026-Q2.

Tasks (36 official + 3 live probes) are grouped GEO, TEMP, SRC, INT, AXIS, SYN. Each has a primary dimension, a success condition, and a hard-fail condition. The agent emits JSON; the harness never grades free-form PDF aesthetics.

## 4. Scoring

See `docs/scoring.md`. Weights match the motivating audit so that a complete, sourced, metro-scoped series with a datetime axis outranks a downtown-labelled, gappy, pretty dashboard.

## 5. Reference agents

Three fixtures ship in `submissions/examples/`:

- `literalist.json` — MREB only, geography tagged metro, 20/20, refuses unpaid core.
- `econometrician.json` — metro plus modeled core at 11.5%, interpolated UrbanPulse tagged, datetime axis, three-regime narrative.
- `extractor.json` — LeaseWatch + chart OCR, categorical axis, truncated 2025, metro numbers labelled core.

These are CI regression tests, not a vendor leaderboard.

## 6. What STRATA-Bench does not measure

Coding skill, tool-use latency, multilingual coverage, or whether an agent can *find* a URL on the live web (except the optional LIVE probe). It measures **epistemic hygiene** under data fragmentation.

## 7. Limitations

v1.0 freezes one metro, one cycle shape, one premium. Agents could overfit the 11.5% figure if they train on this repository; a future v1.1 should draw premiums per seed and hold out a hashed gold split. Live-track scoring is still qualitative.

## 8. Release

Apache-2.0. Code, corpus, scorer, and this note: https://github.com/movahedi-ca/strata-bench
