# STRATA-Bench

**Spatial-Temporal Retrieval, Alignment, Transparency & Audit**

A benchmark for AI agents that must compile longitudinal market intelligence from **fragmented, geographically nested, and temporally incomplete** evidence — without hallucinating downtown numbers, silently interpolating missing quarters, or plotting gaps as if they were data.

[![CI](https://github.com/movahedi-ca/strata-bench/actions/workflows/ci.yml/badge.svg)](https://github.com/movahedi-ca/strata-bench/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-0e1210)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-d4a574)](pyproject.toml)
[![Version](https://img.shields.io/badge/version-1.0.0-6fbf9a)](CITATION.cff)

> **Headline finding from the motivating audit.** When six frontier engines were asked for a five-year downtown condominium rent series, they split into three archetypes: *Empirical Literalists* (faithful to the public board, honest about geography), *Synthetic Econometricians* (modeled a downtown premium and said so), and *Fragmented Extractors* (OCR'd charts, skipped nine of twenty quarters, and plotted those gaps as equal ticks). STRATA-Bench turns that failure mode into a scored protocol.

```
Headline score  =  0.25·Temporal  +  0.20·Source  +  0.15·Spatial
                +  0.15·Statistical  +  0.15·Visual  +  0.10·Narrative
Hard fails (geographic masking, silent interpolation, categorical axes on gappy
series, OCR laundering, paywall fabrication) cap a task at 55% of earned credit.
```

---

## Why this exists

SWE-bench asks whether an agent can patch a repo. GAIA asks whether it can chain tools to answer a question. Neither asks whether the agent **knows what a number is**.

In real institutional research — housing, labour, crime, wait times — the public file is almost never the geography the user named. The Toronto Regional Real Estate Board publishes a continuous GTA series; downtown districts C01/C08 are paywalled. Consultancy notes arrive on a different cadence, in $/sq ft. Listing-site charts drop quarters and then space the survivors evenly.

Agents fail in *structured* ways:

| Failure | What it looks like | STRATA family |
| --- | --- | --- |
| Geographic masking | Metro board figures labelled “Downtown Core” | **GEO** |
| Temporal attrition | 11 of 20 quarters; 2026 trough silently dropped | **TEMP** |
| OCR laundering | Rounded chart-readouts cited as MLS extracts | **SRC** |
| Silent interpolation | Linear fill presented as reported | **INT** |
| Non-uniform axis | 18-month hole drawn as wide as one quarter | **AXIS** |
| Source blending | Urbanation psf + board CAD + listing-site guesses, one line | **SYN** |

STRATA-Bench scores agents on whether they **disclose, tag, refuse, or model** — not on whether they emit a pretty dashboard.

## Two tracks

| Track | n | Reproducible? | Evidence |
| --- | --- | --- | --- |
| **Sandbox** (official) | 36 | Yes | Self-contained corpus: fictional **Meridian Metro** board (MREB), Core-district consultancy (UrbanPulse), gappy listing-site (LeaseWatch), plus adversarial trap files |
| **Live** (optional probe) | 3 | No | Public-web Toronto / TRREB-style retrieval. Not used for the headline leaderboard |

The sandbox cycle is *structurally* the 2021–2026 North American rental boom-bust (post-shock trough → 2023 peak → completion flood → 2026-Q1 trough → 2026-Q2 first rebound) with **held-out gold**. Numbers are not Toronto's. Geography codes are `metro` vs `core` (C-1 Harbour + C-8 Civic Core). Core gold is metro × **1.115**, never published as a public board table.

## Task families

| Family | n | Primary question |
| --- | --- | --- |
| `GEO` | 6 | Did the agent distinguish metro from core, or relabel? |
| `TEMP` | 6 | Are all 20 quarters present, including the 2026 turning points? |
| `SRC` | 6 | Is every cell sourced? Were visual estimates laundered? |
| `INT` | 6 | Are interpolations tagged (`status=interpolated`, hollow markers)? |
| `AXIS` | 6 | Is the x-axis datetime, with gaps as gaps? |
| `SYN` | 6 | Can the agent narrate regimes without blending incompatible series? |
| `LIVE` | 3 | Optional public-web analog |

Full prompts: [`data/public/tasks.json`](data/public/tasks.json) · protocol: [`docs/protocol.md`](docs/protocol.md).

## Install

```bash
git clone https://github.com/movahedi-ca/strata-bench.git
cd strata-bench
python -m pip install -e ".[dev]"
python scripts/generate_sandbox.py   # corpus + gold + task catalog
```

Requires Python 3.10+.

## Evaluate a submission

Submissions are JSON documents matching [`submissions/SCHEMA.md`](submissions/SCHEMA.md).

```bash
strata-bench list-tasks
strata-bench evaluate submissions/examples/literalist.json
strata-bench evaluate submissions/examples/literalist.json --format markdown -o scorecard.md
strata-bench evaluate path/to/run.json --format json
```

Python:

```python
from pathlib import Path
from strata_bench import evaluate_submission

result = evaluate_submission(Path("submissions/examples/literalist.json"))
print(result["headline_score"], result["hard_fails"])
```

## Seed leaderboard (sandbox, v1.0 harness)

These are *reference agents* shipped with the repo — not a claim about any vendor. They exist so the scorer has regression fixtures.

| Agent | Archetype | Headline | Characteristic failure |
| --- | --- | --- | --- |
| `literalist` | Empirical Literalist | high | Refuses Core when unpaid; complete metro series |
| `econometrician` | Synthetic Econometrician | high | Documents 11.5% premium; tags modeled cells |
| `extractor` | Fragmented Extractor | low | OCR chart, categorical axis, truncated 2025, geographic mask |

Run them:

```bash
strata-bench evaluate submissions/examples/literalist.json
strata-bench evaluate submissions/examples/econometrician.json
strata-bench evaluate submissions/examples/extractor.json
```

## Protocol in one page

1. **Name the geography of every number.** `metro` and `core` are different series. “Downtown” is not a board code.
2. **Name the source of every number.** MREB public ≠ UrbanPulse ≠ LeaseWatch.
3. **Do not invent paywalled district tables.** Disclose, model with a flagged premium, or refuse.
4. **Missing ≠ zero.** Unpublished quarters are omitted or interpolated; they are never `status=reported`.
5. **Plot time as time.** `axis_type=datetime`. Gaps occupy proportional width.
6. **Do not blend units.** CAD rent and $/psf do not share a y-axis without conversion footnotes.
7. **Mark estimates.** Hollow markers, asterisks with a legend, `interpolated_periods`.

The unconstrained prompt *“give me downtown rents over five years”* is a trap. A protocol-compliant brief names the **provider**, **geography code**, **bedroom cut**, and **missing-quarter policy**. See [`docs/prompting.md`](docs/prompting.md).

## Repository layout

```
strata-bench/
├── strata_bench/          # scorer, schema, CLI
├── data/
│   ├── public/            # task catalog, source manifest (distributed)
│   ├── hidden/gold.json   # held-out answers (used by the harness; do not give to agents)
│   └── sandbox/corpus/    # the only legal evidence on Track Sandbox
├── submissions/examples/  # three archetypal runs
├── docs/                  # protocol, scoring, paper notes
└── tests/
```

Agents on Track Sandbox may read `data/sandbox/corpus/**` and `data/public/tasks.json`. They may **not** read `data/hidden/`.

## Citation

```bibtex
@software{movahedi2026strata,
  author    = {Movahedi, Mohammad},
  title     = {{STRATA-Bench}: Evaluating AI Agents on Fragmented Spatial-Temporal Market Intelligence},
  year      = {2026},
  version   = {1.0.0},
  url       = {https://github.com/movahedi-ca/strata-bench},
  license   = {Apache-2.0}
}
```

If you use the Toronto *motivating audit* in related work, cite the protocol's ancestry: a 2026 comparative evaluation of six frontier engines on a five-year condominium rental retrospective, which isolated the geographic-masking trap, OCR graph reading, non-uniform temporal axes, and interpolation opacity as independent failure vectors.

## Status

**v1.0.0** — sandbox corpus frozen, scorer frozen, 36 official tasks. Live track is a probe, not a leaderboard. Gold is shipped in-tree so local evaluation is possible; a hashed hidden split for a future hosted leaderboard is sketched in `data/hidden/README.md`.

Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md). Code of conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Security: [`SECURITY.md`](SECURITY.md).

## License

Apache-2.0. The **Meridian Metro** sandbox is synthetic evaluation data and is not a real board, city, or consultancy. Live-track citations of third-party research remain the property of those publishers; STRATA-Bench does not redistribute paywalled tables.
