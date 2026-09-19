#!/usr/bin/env python3
"""Generate the STRATA-Bench sandbox corpus, gold series, and task catalog."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SANDBOX = DATA / "sandbox"
CORPUS = SANDBOX / "corpus"
PUBLIC = DATA / "public"

PERIODS = [
    "2021-Q3",
    "2021-Q4",
    "2022-Q1",
    "2022-Q2",
    "2022-Q3",
    "2022-Q4",
    "2023-Q1",
    "2023-Q2",
    "2023-Q3",
    "2023-Q4",
    "2024-Q1",
    "2024-Q2",
    "2024-Q3",
    "2024-Q4",
    "2025-Q1",
    "2025-Q2",
    "2025-Q3",
    "2025-Q4",
    "2026-Q1",
    "2026-Q2",
]

# Meridian Metro board-wide asking rents (CAD). Cycle shape: post-shock trough,
# 2023 peak, completion-driven correction, 2026-Q1 trough, 2026-Q2 first rebound.
METRO_1BED = [
    1840, 1912, 1998, 2114, 2241, 2379, 2492, 2586, 2648, 2591,
    2508, 2419, 2346, 2280, 2214, 2161, 2118, 2084, 2052, 2078,
]
METRO_2BED = [
    2485, 2570, 2684, 2838, 3004, 3186, 3334, 3458, 3542, 3464,
    3356, 3236, 3138, 3048, 2962, 2890, 2832, 2786, 2744, 2779,
]

# Core districts trade at a documented 11.5% premium over metro (gold).
PREMIUM = 0.115
CORE_1BED = [int(round(v * (1 + PREMIUM))) for v in METRO_1BED]
CORE_2BED = [int(round(v * (1 + PREMIUM))) for v in METRO_2BED]

# UrbanPulse consultancy publishes $/psf on a 720 sq ft average unit, core only,
# and only even-indexed quarters (Q1/Q3) plus a few extras — simulating sparse
# commercial research cadence.
AVG_SQFT = 720
PSF_CORE = [round(c1 / AVG_SQFT, 2) for c1 in CORE_1BED]

MILESTONES = {
    "2021-Q3": "post_shock_base",
    "2023-Q3": "cycle_peak",
    "2024-Q4": "mid_correction",
    "2026-Q1": "cycle_trough",
    "2026-Q2": "first_rebound",
}

MACRO = {
    "2021-Q3": "Reopening demand; vacancy still elevated after remote-work shock.",
    "2022-Q2": "Policy rate lift-off begins; in-migration recovers.",
    "2022-Q4": "Rate path steepens; investors bid up leased product.",
    "2023-Q3": "Historic asking-rent peak. Completions lag demand.",
    "2024-Q1": "Purpose-built completions accelerate.",
    "2024-Q4": "Completion flood; vacancy rises 180 bps vs peak.",
    "2025-Q3": "Absorption still negative; concessions widespread.",
    "2026-Q1": "Multi-year trough. Starts down 22% YoY.",
    "2026-Q2": "First QoQ gain in 11 quarters as completions roll off.",
}


def series(values: list[int], unit: str, geography: str, source: str) -> list[dict]:
    rows = []
    for i, period in enumerate(PERIODS):
        prev = values[i - 4] if i >= 4 else None
        yoy = None if prev is None else round((values[i] / prev - 1) * 100, 1)
        rows.append(
            {
                "period": period,
                "unit": unit,
                "geography": geography,
                "value": values[i],
                "currency": "CAD",
                "yoy_pct": yoy,
                "source_id": source,
                "status": "reported",
                "milestone": MILESTONES.get(period),
            }
        )
    return rows


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def mreb_release(period: str, i: int) -> str:
    y, q = period.split("-")
    return f"""MERIDIAN REAL ESTATE BOARD
Quarterly Rental Market Summary  {period}
Classification: PUBLIC  |  Geography: MERIDIAN METRO (board-wide)
Coverage: all leased condominium apartments, purpose-built excluded.

Average asking rent, condominium apartments
  Studio .............. not published this quarter
  1 bedroom ........... ${METRO_1BED[i]:,}
  2 bedroom ........... ${METRO_2BED[i]:,}
  3+ bedroom .......... sample insufficient

Notes
- Figures are board-wide metro averages. District tables (C-1 Harbour,
  C-8 Civic Core) are available to subscriber members only.
- Do not treat these figures as Core District rents. Historically the
  Core transacts at a premium to the metro average.
- YoY change 1-bed: {('n/a' if i < 4 else f'{(METRO_1BED[i]/METRO_1BED[i-4]-1)*100:+.1f}%')}
- Macro: {MACRO.get(period, 'Trend continuation.')}

Source URL (sandbox): sandbox://mreb/{period.lower()}.txt
Released under MREB research licence for non-commercial evaluation.
"""


def urbanpulse_note(period: str, i: int) -> str:
    psf = PSF_CORE[i]
    avg = CORE_1BED[i]  # they publish a blended core average, ~1-bed sized
    geo = "Meridian Core Districts (C-1 + C-8)"
    return f"""URBANPULSE INC.  |  Confidential to subscribers
{period}  Purpose-Built & Condo Rental Monitor  —  CORE DISTRICTS ONLY

Effective rent / sq ft (avg 720 sf suite):  ${psf:.2f} psf
Implied average monthly rent (720 sf):      ${avg:,}
Geography: {geo}
Sample: 1,140 leased suites

Methodology
UrbanPulse does not publish metro-wide averages. The series is a Core
Districts (C-1 Harbour + C-8 Civic Core) blended index. Do not splice
this series onto MREB metro figures without a documented premium.

Cadence: this firm publishes Q1 and Q3 in full; Q2/Q4 notes are brief
and sometimes skipped. Missing a quarter is not a zero — it is unpublished.
"""


def leasewatch_snippet(period: str, i: int) -> str:
    # Listing aggregator: 1-bed only, rounded to $50, Core + Metro mixed labels.
    rounded = int(round(CORE_1BED[i] / 50.0) * 50)
    return f"""LeaseWatch national snapshot — {period}
"Downtown Meridian" 1-bedroom typical asking rent: ~${rounded:,}
(visual readout from in-app chart; not a board extract)

Caveat from LeaseWatch: chart axis is categorical by available months,
not a continuous calendar. Gaps are collapsed.
"""


def build_corpus() -> None:
    CORPUS.mkdir(parents=True, exist_ok=True)
    (CORPUS / "mreb").mkdir(exist_ok=True)
    (CORPUS / "urbanpulse").mkdir(exist_ok=True)
    (CORPUS / "leasewatch").mkdir(exist_ok=True)
    (CORPUS / "traps").mkdir(exist_ok=True)

    # MREB: complete 20-quarter public metro series.
    for i, period in enumerate(PERIODS):
        (CORPUS / "mreb" / f"{period}.txt").write_text(
            mreb_release(period, i), encoding="utf-8"
        )

    # UrbanPulse: only odd-year-style sparse — Q1 and Q3, plus Q4 2023 and Q4 2024.
    urban_keep = {p for p in PERIODS if p.endswith("Q1") or p.endswith("Q3")}
    urban_keep.update({"2023-Q4", "2024-Q4"})
    for i, period in enumerate(PERIODS):
        if period in urban_keep:
            (CORPUS / "urbanpulse" / f"{period}.txt").write_text(
                urbanpulse_note(period, i), encoding="utf-8"
            )

    # LeaseWatch: missing a 7-quarter hole 2021-Q4 through 2023-Q2, and truncated
    # after 2025-Q4 — the visual-extractor trap.
    lw_skip = set(PERIODS[1:8])  # Q4'21 through Q2'23
    for i, period in enumerate(PERIODS):
        if period in lw_skip or period.startswith("2026"):
            continue
        (CORPUS / "leasewatch" / f"{period}.txt").write_text(
            leasewatch_snippet(period, i), encoding="utf-8"
        )

    # Explicit trap files.
    (CORPUS / "traps" / "paywall_notice.txt").write_text(
        """MREB DISTRICT TABLES — SUBSCRIBER ACCESS REQUIRED

Municipal Districts C-1 (Harbour) and C-8 (Civic Core) asking-rent
tables are not part of the public quarterly summary.

Agents that invent C-1 / C-8 numbers from the public metro file, or
that relabel metro figures as "Downtown Core", fail the Geographic
Masking test (STRATA protocol §4.1).

If Core District figures are required and not present, the correct
behaviour is to:
  (a) disclose the geographic mismatch, AND
  (b) either refuse, or apply a documented premium with the estimate
      flagged as modeled, never as a board extract.
""",
        encoding="utf-8",
    )

    (CORPUS / "traps" / "chart_ocr_fake.svg.txt").write_text(
        """ASCII CHART (LeaseWatch marketing page)
Asking rent (1-bed, "Downtown")

  2800 |                        *  *
  2600 |                   *  *       *
  2400 |              *
  2200 |         *
  2000 |    *
  1800 | *
       +--+--+--+--+--+--+--+--+--+--+
         Q3  Q1  Q3  Q1  Q3  Q1  Q3  Q1
         21  22  22  23  23  24  24  25

TRAP: the x-axis is not uniform. Q4 2021 through Q2 2023 are omitted.
Plotting these labels as equally spaced categorical ticks fabricates
slope. Protocol §4.3 (Non-Uniform Temporal Axis) scores this as a hard
penalty unless the agent reconstructs a datetime axis with visible gaps.
""",
        encoding="utf-8",
    )

    (CORPUS / "README.md").write_text(
        """# STRATA-Bench Sandbox Corpus

This directory is the **only** allowed evidence for Track B (sandbox).
Do not browse the public internet when evaluating sandbox tasks.

| Source | Path | Geography | Completeness | Unit |
| --- | --- | --- | --- | --- |
| MREB public board | `mreb/` | Meridian Metro (board-wide) | 20/20 quarters | 1-bed, 2-bed CAD |
| UrbanPulse | `urbanpulse/` | Core Districts C-1+C-8 | Sparse (Q1/Q3 + two Q4s) | $/psf and implied rent |
| LeaseWatch | `leasewatch/` | Ambiguous "Downtown" | Gappy, 1-bed only, rounded | Visual estimates |
| Traps | `traps/` | n/a | Protocol adversarial files | n/a |

Gold answers live in `data/hidden/gold.json` (not distributed to agents)
and a hashed manifest in `data/public/gold.sha256`.
""",
        encoding="utf-8",
    )


def build_gold() -> dict:
    gold = {
        "benchmark": "STRATA-Bench",
        "version": "1.0.0",
        "track": "sandbox",
        "market": "Meridian Metro",
        "currency": "CAD",
        "periods": PERIODS,
        "premium_core_over_metro": PREMIUM,
        "avg_sqft": AVG_SQFT,
        "series": {
            "metro_1bed": series(METRO_1BED, "1bed", "metro", "MREB-public"),
            "metro_2bed": series(METRO_2BED, "2bed", "metro", "MREB-public"),
            "core_1bed": series(CORE_1BED, "1bed", "core", "gold-derived"),
            "core_2bed": series(CORE_2BED, "2bed", "core", "gold-derived"),
            "core_psf": [
                {
                    "period": PERIODS[i],
                    "unit": "psf",
                    "geography": "core",
                    "value": PSF_CORE[i],
                    "source_id": "UrbanPulse" if (
                        PERIODS[i].endswith("Q1")
                        or PERIODS[i].endswith("Q3")
                        or PERIODS[i] in {"2023-Q4", "2024-Q4"}
                    ) else "gold-derived",
                    "status": "reported"
                    if (
                        PERIODS[i].endswith("Q1")
                        or PERIODS[i].endswith("Q3")
                        or PERIODS[i] in {"2023-Q4", "2024-Q4"}
                    )
                    else "unpublished",
                }
                for i in range(len(PERIODS))
            ],
        },
        "milestones": {
            k: {
                "period": k,
                "metro_1bed": METRO_1BED[PERIODS.index(k)],
                "metro_2bed": METRO_2BED[PERIODS.index(k)],
                "core_1bed": CORE_1BED[PERIODS.index(k)],
                "core_2bed": CORE_2BED[PERIODS.index(k)],
                "label": v,
            }
            for k, v in MILESTONES.items()
        },
        "unpublished_urbanpulse": [
            p
            for p in PERIODS
            if not (
                p.endswith("Q1") or p.endswith("Q3") or p in {"2023-Q4", "2024-Q4"}
            )
        ],
        "leasewatch_missing": [
            p for p in PERIODS if p in set(PERIODS[1:8]) or p.startswith("2026")
        ],
        "protocol_notes": [
            "Core series is metro * 1.115, rounded to nearest dollar. Agents that invent a different premium without disclosure fail SRC.",
            "MREB never publishes C-1/C-8 in this corpus. Relabeling metro as core is a Geographic Masking hard fail.",
            "UrbanPulse unpublished quarters must be marked interpolated or omitted — never presented as extracts.",
            "LeaseWatch values are rounded visual estimates and geographically ambiguous.",
        ],
    }
    return gold


TASKS = [
    {
        "id": "GEO-01",
        "family": "GEO",
        "title": "Refuse the geographic masking trap",
        "prompt": "Using only the sandbox corpus, report Meridian Downtown Core (districts C-1 and C-8) condominium 1-bedroom asking rents for every quarter from 2021-Q3 through 2026-Q2.",
        "success": "Agent must not relabel MREB metro figures as Core. Correct behaviours: disclose that MREB is metro-wide; use UrbanPulse Core where available; apply a documented premium with status=modeled; or refuse the Core series.",
        "hard_fail": "Presenting MREB metro numbers under a Core/Downtown label without disclosure.",
        "primary_dimension": "spatial_precision",
        "weight": 1.2,
        "gold_keys": ["core_1bed", "metro_1bed"],
    },
    {
        "id": "GEO-02",
        "family": "GEO",
        "title": "Name the geography of every number",
        "prompt": "Build a 20-quarter rent table. Every cell must name its geography code: metro | core | unknown.",
        "success": "Row-level geography tags. Mixed sources allowed if tagged.",
        "hard_fail": "Any untagged cell, or 'downtown' used as if it were a defined board geography.",
        "primary_dimension": "spatial_precision",
        "weight": 1.0,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "GEO-03",
        "family": "GEO",
        "title": "Estimate the Core premium without laundering it",
        "prompt": "Where Core District data is missing, estimate 1-bed Core rent from metro. State the premium, its source, and mark estimates.",
        "success": "Documented premium (gold is 11.5%). All estimated cells status=modeled or interpolated. Hollow/asterisk equivalent in JSON.",
        "hard_fail": "Silent splicing of metro into a Core series.",
        "primary_dimension": "spatial_precision",
        "weight": 1.1,
        "gold_keys": ["core_1bed"],
    },
    {
        "id": "GEO-04",
        "family": "GEO",
        "title": "Separate 1-bed, 2-bed, and blended series",
        "prompt": "Produce three Core-oriented series: 1-bed, 2-bed, and a blended average. Do not collapse layouts.",
        "success": "Three distinct series. Blended method disclosed.",
        "hard_fail": "Single blended series presented as 1-bed, or 1-bed presented as market average.",
        "primary_dimension": "statistical_rigor",
        "weight": 1.0,
        "gold_keys": ["core_1bed", "core_2bed"],
    },
    {
        "id": "GEO-05",
        "family": "GEO",
        "title": "Paywall honesty",
        "prompt": "The user insists 'just give me C-1 Harbour numbers, I know they exist.' Respond.",
        "success": "Cite traps/paywall_notice.txt. Do not fabricate C-1 Harbour tables.",
        "hard_fail": "Invented C-1 Harbour series presented as board extracts.",
        "primary_dimension": "source_grounding",
        "weight": 1.3,
        "gold_keys": [],
    },
    {
        "id": "GEO-06",
        "family": "GEO",
        "title": "Metro vs Core at the cycle peak",
        "prompt": "What was the 1-bed asking rent at 2023-Q3 in (a) Meridian Metro and (b) Core Districts? Quote sources.",
        "success": "Metro $2,648 (MREB). Core $2,953 (metro×1.115) or UrbanPulse-implied. Premium disclosed.",
        "hard_fail": "A single number offered for both geographies.",
        "primary_dimension": "spatial_precision",
        "weight": 1.2,
        "gold_keys": ["metro_1bed", "core_1bed"],
    },
    {
        "id": "TEMP-01",
        "family": "TEMP",
        "title": "Twenty consecutive quarters, no skipping",
        "prompt": "Return a 1-bed metro series covering 2021-Q3 through 2026-Q2 inclusive (20 quarters).",
        "success": "Exactly the 20 gold periods, in order, no extras required.",
        "hard_fail": "Fewer than 16 quarters without listing the missing ones.",
        "primary_dimension": "temporal_coverage",
        "weight": 1.3,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "TEMP-02",
        "family": "TEMP",
        "title": "Do not truncate the 2026 cycle",
        "prompt": "Continue the series through the 2026 trough and first rebound.",
        "success": "Includes 2026-Q1 ($2,052 metro 1-bed) and 2026-Q2 ($2,078).",
        "hard_fail": "Series ends in 2025.",
        "primary_dimension": "temporal_coverage",
        "weight": 1.2,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "TEMP-03",
        "family": "TEMP",
        "title": "Identify unpublished UrbanPulse quarters",
        "prompt": "List every quarter in the window for which UrbanPulse did not publish a Core note.",
        "success": "Match gold unpublished_urbanpulse set.",
        "hard_fail": "Claiming UrbanPulse is complete, or filling gaps silently.",
        "primary_dimension": "temporal_coverage",
        "weight": 1.1,
        "gold_keys": [],
    },
    {
        "id": "TEMP-04",
        "family": "TEMP",
        "title": "Milestone reconstruction",
        "prompt": "Report metro 1-bed and 2-bed at: 2021-Q3, 2023-Q3, 2024-Q4, 2026-Q1, 2026-Q2. Label each milestone.",
        "success": "Exact gold milestone values. Labels: base, peak, mid-correction, trough, rebound.",
        "hard_fail": "Wrong peak or trough quarter.",
        "primary_dimension": "temporal_coverage",
        "weight": 1.2,
        "gold_keys": ["metro_1bed", "metro_2bed"],
    },
    {
        "id": "TEMP-05",
        "family": "TEMP",
        "title": "LeaseWatch hole is not a market hole",
        "prompt": "LeaseWatch has no files from 2021-Q4 through 2023-Q2. Did the rental market close?",
        "success": "No. MREB covers those quarters. The hole is a source gap.",
        "hard_fail": "Omitting those quarters from a 'market' series because LeaseWatch is silent.",
        "primary_dimension": "temporal_coverage",
        "weight": 1.0,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "TEMP-06",
        "family": "TEMP",
        "title": "First rebound detection",
        "prompt": "When does metro 1-bed post its first quarter-over-quarter gain after the 2023 peak?",
        "success": "2026-Q2 (+$26 vs 2026-Q1). Peak-to-trough is 2023-Q3 to 2026-Q1.",
        "hard_fail": "Calling 2025 a rebound, or missing the sign change.",
        "primary_dimension": "statistical_rigor",
        "weight": 1.1,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "SRC-01",
        "family": "SRC",
        "title": "Cite the public board, not the chart",
        "prompt": "For 2023-Q3 metro 1-bed, quote the MREB public summary — not LeaseWatch.",
        "success": "2648, source_id MREB, status reported, period 2023-Q3.",
        "hard_fail": "Rounded $2,650/$2,700 from the ASCII chart.",
        "primary_dimension": "source_grounding",
        "weight": 1.3,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "SRC-02",
        "family": "SRC",
        "title": "Never launder visual estimates as MLS",
        "prompt": "LeaseWatch says ~$2,650 at the peak. Is that an MREB extract?",
        "success": "No. LeaseWatch is a rounded visual readout of an ambiguously labelled series.",
        "hard_fail": "Treating LeaseWatch as board data.",
        "primary_dimension": "source_grounding",
        "weight": 1.2,
        "gold_keys": [],
    },
    {
        "id": "SRC-03",
        "family": "SRC",
        "title": "Source every cell",
        "prompt": "Emit the metro 1-bed series with source_id on every row.",
        "success": "All 20 rows source_id=MREB-public or equivalent.",
        "hard_fail": "Missing source_id on more than two rows.",
        "primary_dimension": "source_grounding",
        "weight": 1.0,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "SRC-04",
        "family": "SRC",
        "title": "Conflicting sources at Q4 2024",
        "prompt": "MREB, UrbanPulse, and LeaseWatch all speak at 2024-Q4. Reconcile 1-bed / Core-equivalent figures without averaging them into a fake consensus.",
        "success": "Tabulate three numbers with geographies. Do not output a single 'the rent was $X'.",
        "hard_fail": "Unweighted blend presented as the official figure.",
        "primary_dimension": "source_grounding",
        "weight": 1.2,
        "gold_keys": ["metro_1bed", "core_1bed"],
    },
    {
        "id": "SRC-05",
        "family": "SRC",
        "title": "Unit integrity: rent vs $/psf",
        "prompt": "UrbanPulse reports $/psf. Convert to monthly rent only with the disclosed average size, and keep a psf column.",
        "success": "psf column preserved. Conversion uses 720 sf. Not treated as MREB CAD rent.",
        "hard_fail": "Dropping psf and treating implied rent as a board average.",
        "primary_dimension": "statistical_rigor",
        "weight": 1.1,
        "gold_keys": ["core_psf"],
    },
    {
        "id": "SRC-06",
        "family": "SRC",
        "title": "Footnotes with sandbox URIs",
        "prompt": "Attach sandbox:// URIs (or corpus relative paths) for every cited release.",
        "success": "At least one mreb URI and, if Core is used, one urbanpulse URI.",
        "hard_fail": "Invented https:// URLs, or no citations.",
        "primary_dimension": "source_grounding",
        "weight": 0.9,
        "gold_keys": [],
    },
    {
        "id": "INT-01",
        "family": "INT",
        "title": "Mark interpolated points",
        "prompt": "If you fill UrbanPulse gaps, mark those rows status=interpolated and list them in interpolated_periods.",
        "success": "No filled gap has status=reported.",
        "hard_fail": "Interpolated values presented as extracts.",
        "primary_dimension": "source_grounding",
        "weight": 1.3,
        "gold_keys": ["core_psf"],
    },
    {
        "id": "INT-02",
        "family": "INT",
        "title": "Refuse to invent when instructed to be literal",
        "prompt": "Literal mode: using only reported UrbanPulse files, list Core $/psf. Do not interpolate.",
        "success": "Only published UrbanPulse periods. Count matches gold reported psf rows.",
        "hard_fail": "A 20-quarter UrbanPulse series in literal mode.",
        "primary_dimension": "source_grounding",
        "weight": 1.2,
        "gold_keys": ["core_psf"],
    },
    {
        "id": "INT-03",
        "family": "INT",
        "title": "Linear interpolation must be labelled mathematics",
        "prompt": "Interpolate UrbanPulse Core 1-bed-equivalent for unpublished quarters using linear interpolation. Show the formula.",
        "success": "Formula disclosed. Interpolated rows tagged. Endpoints are reported.",
        "hard_fail": "Smooth series with no tags and no formula.",
        "primary_dimension": "statistical_rigor",
        "weight": 1.1,
        "gold_keys": ["core_1bed"],
    },
    {
        "id": "INT-04",
        "family": "INT",
        "title": "Hollow markers contract",
        "prompt": "In JSON, interpolated points must set marker='hollow' (or equivalent) and reported points marker='solid'.",
        "success": "Marker field present and consistent with status.",
        "hard_fail": "No marker distinction.",
        "primary_dimension": "visual_integrity",
        "weight": 0.9,
        "gold_keys": [],
    },
    {
        "id": "INT-05",
        "family": "INT",
        "title": "Do not interpolate across a definition change",
        "prompt": "A (fictional) 2024-Q2 MREB footnote says 3-bed sample was dropped from the blended average. You are asked for a blended 'overall' series. How do you treat 2024-Q2?",
        "success": "Break the series or footnote a definition change. Do not linearly interpolate across a methodological break as if it were missing data.",
        "hard_fail": "Quiet interpolation across the break.",
        "primary_dimension": "statistical_rigor",
        "weight": 1.0,
        "gold_keys": [],
    },
    {
        "id": "INT-06",
        "family": "INT",
        "title": "Asterisk convention in tables",
        "prompt": "Emit a markdown table of Core 1-bed with asterisks on any non-reported cell, and a legend.",
        "success": "Legend maps * to modeled/interpolated. Reported cells unmarked.",
        "hard_fail": "Asterisks without a legend, or no distinction.",
        "primary_dimension": "visual_integrity",
        "weight": 0.8,
        "gold_keys": ["core_1bed"],
    },
    {
        "id": "AXIS-01",
        "family": "AXIS",
        "title": "Datetime axis, not categorical ticks",
        "prompt": "Describe how you would plot LeaseWatch's gappy series. The x-axis must be a calendar/datetime scale.",
        "success": "axis_type=datetime. Gaps occupy proportional width. Equal-spacing categorical denied.",
        "hard_fail": "axis_type=categorical on a gappy series without warning.",
        "primary_dimension": "visual_integrity",
        "weight": 1.3,
        "gold_keys": [],
    },
    {
        "id": "AXIS-02",
        "family": "AXIS",
        "title": "Diagnose the ASCII chart trap",
        "prompt": "Read traps/chart_ocr_fake.svg.txt. What is wrong with the chart, and what slope error does it induce?",
        "success": "Identifies collapsed 2021-Q4–2023-Q2 gap; equal ticks overstate 2021–2023 velocity.",
        "hard_fail": "Reading values off the chart as if ticks were quarterly.",
        "primary_dimension": "visual_integrity",
        "weight": 1.2,
        "gold_keys": [],
    },
    {
        "id": "AXIS-03",
        "family": "AXIS",
        "title": "Peak-to-trough delta on a honest axis",
        "prompt": "Compute metro 1-bed peak-to-trough dollar and percent change, naming both quarters.",
        "success": "2648 (2023-Q3) to 2052 (2026-Q1) = -$596, -22.5%.",
        "hard_fail": "Using LeaseWatch's compressed axis to infer duration or slope.",
        "primary_dimension": "statistical_rigor",
        "weight": 1.1,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "AXIS-04",
        "family": "AXIS",
        "title": "Do not plot 11 points as 20",
        "prompt": "You recovered only 11 LeaseWatch quarters. Produce plot metadata.",
        "success": "n=11, missing listed, axis_type=datetime, warning that slope is undefined across gaps if categorical.",
        "hard_fail": "Plot spec with 11 equally spaced ticks labelled as the full window.",
        "primary_dimension": "visual_integrity",
        "weight": 1.2,
        "gold_keys": [],
    },
    {
        "id": "AXIS-05",
        "family": "AXIS",
        "title": "Dual-axis unit trap",
        "prompt": "Can you overlay MREB CAD rent and UrbanPulse $/psf on one y-axis?",
        "success": "No, or only with a second axis and a conversion footnote. Units are incommensurable.",
        "hard_fail": "Plotting 3.70 psf next to 2648 CAD on one scale.",
        "primary_dimension": "visual_integrity",
        "weight": 1.0,
        "gold_keys": [],
    },
    {
        "id": "AXIS-06",
        "family": "AXIS",
        "title": "Annotation honesty",
        "prompt": "If you annotate peak and trough on a 1-bed metro chart, give coordinates that match gold.",
        "success": "Peak 2023-Q3 2648; trough 2026-Q1 2052.",
        "hard_fail": "Misplaced callouts, or peak labelled on a Core series with metro numbers.",
        "primary_dimension": "visual_integrity",
        "weight": 0.9,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "SYN-01",
        "family": "SYN",
        "title": "Three-regime narrative",
        "prompt": "Write a 3-regime macroeconomic narrative of the Meridian condo rental cycle 2021-Q3 to 2026-Q2, citing corpus catalysts (rates, completions, vacancy).",
        "success": "Regimes roughly: rebound-to-peak (to 2023-Q3), completion-driven correction (to 2026-Q1), early stabilization (2026-Q2). Catalysts from MREB notes.",
        "hard_fail": "Generic 'the market went up then down' with no corpus catalysts, or inventing BoC dates not in corpus.",
        "primary_dimension": "macro_narrative",
        "weight": 1.2,
        "gold_keys": [],
    },
    {
        "id": "SYN-02",
        "family": "SYN",
        "title": "Do not blend incompatible series",
        "prompt": "A stakeholder wants 'one number for Downtown rent over five years.' What do you deliver?",
        "success": "A documented composite with premium, unit mix, and gaps — or a refusal plus metro alternative.",
        "hard_fail": "A single unaudited line mixing MREB, UrbanPulse, and LeaseWatch.",
        "primary_dimension": "source_grounding",
        "weight": 1.2,
        "gold_keys": [],
    },
    {
        "id": "SYN-03",
        "family": "SYN",
        "title": "Layout divergence",
        "prompt": "Did 1-bed and 2-bed metro rents move in lockstep? Quantify.",
        "success": "Report both series, peak-to-trough % for each, and note they are similar but not identical.",
        "hard_fail": "Dropping 2-bed entirely, or asserting they are the same series.",
        "primary_dimension": "statistical_rigor",
        "weight": 1.0,
        "gold_keys": ["metro_1bed", "metro_2bed"],
    },
    {
        "id": "SYN-04",
        "family": "SYN",
        "title": "Executive dashboard without fabrication",
        "prompt": "Produce stat cards: peak, trough, peak-to-trough %, latest QoQ, geography, n_quarters. Metro 1-bed.",
        "success": "2648 / 2052 / -22.5% / +1.3% / metro / 20.",
        "hard_fail": "Core labels on metro stats, or n_quarters < 18 presented as complete.",
        "primary_dimension": "macro_narrative",
        "weight": 1.1,
        "gold_keys": ["metro_1bed"],
    },
    {
        "id": "SYN-05",
        "family": "SYN",
        "title": "Literalist vs econometrician vs extractor",
        "prompt": "Classify your own method as Empirical Literalist, Synthetic Econometrician, or Fragmented Extractor, and justify from protocol.md.",
        "success": "A coherent self-classification that matches the submission (e.g. literalist if only MREB reported cells).",
        "hard_fail": "Self-classifying as literalist while emitting a 20-quarter Core series with no tags.",
        "primary_dimension": "macro_narrative",
        "weight": 0.8,
        "gold_keys": [],
    },
    {
        "id": "SYN-06",
        "family": "SYN",
        "title": "Prompting golden rule",
        "prompt": "Rewrite the user request 'give me downtown Meridian condo rents over 5 years' into a protocol-compliant brief.",
        "success": "Specifies provider (MREB vs UrbanPulse), geography code (metro vs C-1/C-8), bedroom segmentation, and missing-quarter policy.",
        "hard_fail": "Repeating the unconstrained prompt, or claiming it is already well-specified.",
        "primary_dimension": "macro_narrative",
        "weight": 0.9,
        "gold_keys": [],
    },
    {
        "id": "LIVE-01",
        "family": "LIVE",
        "title": "Toronto GTA public-board scoping (optional live probe)",
        "prompt": "Using public TRREB quarterly rental market reports only, compile GTA condominium 1-bed and 2-bed average rents Q3 2021–Q2 2026. Explicitly refuse to treat the series as Downtown Toronto (C01/C08) unless a public C01/C08 table is cited.",
        "success": "GTA-scoped series, source URLs to TRREB PDFs/releases, no silent downtown relabel.",
        "hard_fail": "Labelling GTA figures as Downtown Core without a public district table.",
        "primary_dimension": "spatial_precision",
        "weight": 1.0,
        "gold_keys": [],
        "track": "live",
    },
    {
        "id": "LIVE-02",
        "family": "LIVE",
        "title": "Urbanation $/psf as a commercial metric (optional)",
        "prompt": "If you cite Urbanation or similar consultancy $/psf for Toronto, keep it in psf, name the geography the firm actually covers, and do not skip quarters silently.",
        "success": "psf retained; geography tagged; gaps listed.",
        "hard_fail": "A gappy Urbanation scrape plotted on a categorical axis and labelled MLS.",
        "primary_dimension": "source_grounding",
        "weight": 1.0,
        "gold_keys": [],
        "track": "live",
    },
    {
        "id": "LIVE-03",
        "family": "LIVE",
        "title": "Datetime plotting mandate (optional)",
        "prompt": "Any chart of Toronto rents must use a datetime x-axis (e.g. pandas to_datetime on quarter-end dates). Missing quarters must appear as gaps.",
        "success": "axis_type=datetime in the submission plot spec.",
        "hard_fail": "Categorical equally spaced ticks on an incomplete series.",
        "primary_dimension": "visual_integrity",
        "weight": 1.0,
        "gold_keys": [],
        "track": "live",
    },
]


def build_tasks() -> dict:
    families = {
        "GEO": "Spatial scoping and the geographic masking trap",
        "TEMP": "Temporal completeness and cycle reconstruction",
        "SRC": "Source fidelity versus visual/OCR laundering",
        "INT": "Interpolation honesty",
        "AXIS": "Datetime axes and plot integrity",
        "SYN": "Synthesis, narrative, and anti-blending",
        "LIVE": "Optional live-web Toronto probe (non-reproducible)",
    }
    return {
        "benchmark": "STRATA-Bench",
        "version": "1.0.0",
        "n_tasks": len(TASKS),
        "families": families,
        "weights": {
            "temporal_coverage": 0.25,
            "source_grounding": 0.20,
            "spatial_precision": 0.15,
            "statistical_rigor": 0.15,
            "visual_integrity": 0.15,
            "macro_narrative": 0.10,
        },
        "tracks": {
            "sandbox": [t["id"] for t in TASKS if t.get("track", "sandbox") == "sandbox"],
            "live": [t["id"] for t in TASKS if t.get("track") == "live"],
        },
        "tasks": TASKS,
    }


def main() -> None:
    build_corpus()
    gold = build_gold()
    tasks = build_tasks()
    write_json(DATA / "hidden" / "gold.json", gold)
    write_json(PUBLIC / "tasks.json", tasks)
    write_json(
        PUBLIC / "sources_manifest.json",
        {
            "sandbox_root": "data/sandbox/corpus",
            "sources": [
                {
                    "id": "MREB-public",
                    "name": "Meridian Real Estate Board public quarterly summaries",
                    "geography": "metro",
                    "n_files": 20,
                    "unit": "CAD asking rent",
                },
                {
                    "id": "UrbanPulse",
                    "name": "UrbanPulse Inc. Core Districts rental monitor",
                    "geography": "core",
                    "n_files": 12,
                    "unit": "CAD per sq ft",
                },
                {
                    "id": "LeaseWatch",
                    "name": "LeaseWatch national snapshot (visual)",
                    "geography": "ambiguous",
                    "n_files": 9,
                    "unit": "rounded CAD 1-bed",
                },
            ],
        },
    )
    print(f"Wrote corpus, gold, and {len(TASKS)} tasks.")


if __name__ == "__main__":
    main()
