#!/usr/bin/env python3
"""Build the three archetypal example submissions from gold + tasks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = json.loads((ROOT / "data" / "hidden" / "gold.json").read_text())
TASKS = json.loads((ROOT / "data" / "public" / "tasks.json").read_text())["tasks"]
OUT = ROOT / "submissions" / "examples"

PERIODS = GOLD["periods"]
METRO_1 = {r["period"]: r["value"] for r in GOLD["series"]["metro_1bed"]}
METRO_2 = {r["period"]: r["value"] for r in GOLD["series"]["metro_2bed"]}
CORE_1 = {r["period"]: r["value"] for r in GOLD["series"]["core_1bed"]}
CORE_2 = {r["period"]: r["value"] for r in GOLD["series"]["core_2bed"]}
PSF = GOLD["series"]["core_psf"]
UNPUB_UP = set(GOLD["unpublished_urbanpulse"])
LW_MISS = set(GOLD["leasewatch_missing"])


def dump(name: str, obj: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def obs(period, value, unit, geo, source, status, marker="solid"):
    return {
        "period": period,
        "unit": unit,
        "value": value,
        "geography": geo,
        "source_id": source,
        "status": status,
        "marker": marker,
    }


def metro_series(unit="1bed"):
    src = METRO_1 if unit == "1bed" else METRO_2
    return [obs(p, src[p], unit, "metro", "MREB-public", "reported") for p in PERIODS]


def literalist() -> dict:
    tasks = {}
    refuse = (
        "MREB public files cover Meridian Metro only. C-1/C-8 (core) tables are "
        "paywalled (sandbox://traps/paywall_notice.txt). I will not relabel metro "
        "figures as downtown. UrbanPulse covers core in $/psf on a sparse cadence."
    )
    tasks["GEO-01"] = {
        "geography": "metro",
        "geography_label": "Meridian Metro (board-wide); Core not in public MREB",
        "series": metro_series(),
        "disclaimers": [refuse],
        "citations": ["sandbox://mreb/2023-q3.txt", "sandbox://traps/paywall_notice.txt"],
        "axis_type": "datetime",
        "narrative": refuse,
        "method_archetype": "empirical_literalist",
    }
    tasks["GEO-02"] = {
        "geography": "metro",
        "series": metro_series(),
        "disclaimers": ["Every cell tagged geography=metro."],
        "citations": ["sandbox://mreb/2021-q3.txt"],
        "axis_type": "datetime",
    }
    tasks["GEO-03"] = {
        "geography": "metro",
        "series": metro_series(),
        "disclaimers": [
            "Literal mode: I refuse to invent a core premium. Gold premium is not a public MREB figure."
        ],
        "omitted_periods": [],
        "citations": ["sandbox://traps/paywall_notice.txt"],
        "axis_type": "datetime",
        "narrative": "Will not estimate core without an instructed premium. Metro series provided instead.",
    }
    tasks["GEO-04"] = {
        "geography": "metro",
        "series": metro_series("1bed") + metro_series("2bed"),
        "disclaimers": ["1-bed and 2-bed kept separate. No blended series fabricated for core."],
        "citations": ["sandbox://mreb/2023-q3.txt"],
        "axis_type": "datetime",
    }
    tasks["GEO-05"] = {
        "geography": "metro",
        "series": [],
        "disclaimers": [refuse],
        "citations": ["sandbox://traps/paywall_notice.txt"],
        "narrative": refuse,
        "axis_type": "datetime",
    }
    tasks["GEO-06"] = {
        "geography": "metro",
        "series": [
            obs("2023-Q3", METRO_1["2023-Q3"], "1bed", "metro", "MREB-public", "reported"),
        ],
        "disclaimers": [
            "Metro 1-bed 2023-Q3 is $2,648 (MREB). Core is not in the public board; I will not quote a core number as an extract."
        ],
        "citations": ["sandbox://mreb/2023-q3.txt"],
        "extras": {"metro_1bed_peak": METRO_1["2023-Q3"]},
        "narrative": "Peak metro 1-bed $2,648 at 2023-Q3. Core withheld (paywall).",
        "axis_type": "datetime",
    }
    tasks["TEMP-01"] = {
        "geography": "metro",
        "series": metro_series(),
        "citations": [f"sandbox://mreb/{p.lower()}.txt" for p in PERIODS],
        "axis_type": "datetime",
        "plot": {"axis_type": "datetime", "missing_periods_shown_as_gaps": True},
    }
    tasks["TEMP-02"] = dict(tasks["TEMP-01"])
    tasks["TEMP-03"] = {
        "geography": "core",
        "series": [],
        "omitted_periods": sorted(UNPUB_UP),
        "disclaimers": ["UrbanPulse unpublished quarters listed in omitted_periods."],
        "citations": ["sandbox://urbanpulse/2023-q3.txt"],
        "narrative": "UrbanPulse publishes Q1/Q3 plus 2023-Q4 and 2024-Q4. Other quarters are unpublished, not zero.",
        "axis_type": "datetime",
    }
    tasks["TEMP-04"] = {
        "geography": "metro",
        "series": [
            obs(p, METRO_1[p], "1bed", "metro", "MREB-public", "reported")
            for p in ["2021-Q3", "2023-Q3", "2024-Q4", "2026-Q1", "2026-Q2"]
        ]
        + [
            obs(p, METRO_2[p], "2bed", "metro", "MREB-public", "reported")
            for p in ["2021-Q3", "2023-Q3", "2024-Q4", "2026-Q1", "2026-Q2"]
        ],
        "narrative": "Milestones: 2021-Q3 post-shock base, 2023-Q3 cycle peak, 2024-Q4 mid-correction, 2026-Q1 trough, 2026-Q2 first rebound.",
        "citations": ["sandbox://mreb/2023-q3.txt", "sandbox://mreb/2026-q1.txt"],
        "axis_type": "datetime",
    }
    tasks["TEMP-05"] = {
        "geography": "metro",
        "series": metro_series(),
        "disclaimers": [
            "LeaseWatch's 2021-Q4–2023-Q2 hole is a source gap. MREB covers those quarters. The market did not close."
        ],
        "narrative": "LeaseWatch hole is not a market hole. Metro series is complete via MREB.",
        "citations": ["sandbox://mreb/2022-q1.txt"],
        "axis_type": "datetime",
    }
    tasks["TEMP-06"] = {
        "geography": "metro",
        "series": metro_series(),
        "narrative": "First QoQ gain after the 2023-Q3 peak is 2026-Q2 (2078 vs 2052). Peak-to-trough is 2023-Q3 to 2026-Q1.",
        "citations": ["sandbox://mreb/2026-q2.txt"],
        "axis_type": "datetime",
        "extras": {"peak_to_trough_pct": -22.5},
    }
    tasks["SRC-01"] = {
        "geography": "metro",
        "series": [obs("2023-Q3", 2648, "1bed", "metro", "MREB-public", "reported")],
        "citations": ["sandbox://mreb/2023-q3.txt"],
        "disclaimers": ["Not LeaseWatch. Board extract."],
        "narrative": "MREB metro 1-bed 2023-Q3 is 2648.",
        "axis_type": "datetime",
    }
    tasks["SRC-02"] = {
        "geography": "metro",
        "series": [],
        "disclaimers": [
            "LeaseWatch ~$2,650 is a rounded visual readout of an ambiguously labelled downtown series. It is not an MREB extract."
        ],
        "citations": ["sandbox://leasewatch/2023-q3.txt", "sandbox://mreb/2023-q3.txt"],
        "narrative": "No. LeaseWatch is not the board. MREB says 2648 metro 1-bed.",
        "axis_type": "datetime",
    }
    tasks["SRC-03"] = {
        "geography": "metro",
        "series": metro_series(),
        "citations": ["sandbox://mreb/2021-q3.txt"],
        "axis_type": "datetime",
    }
    tasks["SRC-04"] = {
        "geography": "mixed",
        "series": [
            obs("2024-Q4", METRO_1["2024-Q4"], "1bed", "metro", "MREB-public", "reported"),
            obs("2024-Q4", CORE_1["2024-Q4"], "1bed", "core", "gold-derived", "modeled"),
        ],
        "disclaimers": [
            "Three sources, three geographies. I will not emit a consensus average. MREB metro 1-bed $2,280; Core modeled at 11.5% if required; LeaseWatch is a rounded visual estimate of an ambiguous downtown label."
        ],
        "citations": [
            "sandbox://mreb/2024-q4.txt",
            "sandbox://urbanpulse/2024-q4.txt",
            "sandbox://leasewatch/2024-q4.txt",
        ],
        "narrative": "Do not average MREB, UrbanPulse, and LeaseWatch.",
        "axis_type": "datetime",
    }
    tasks["SRC-05"] = {
        "geography": "core",
        "series": [
            {
                "period": r["period"],
                "unit": "psf",
                "value": r["value"],
                "geography": "core",
                "source_id": r["source_id"],
                "status": r["status"] if r["status"] == "reported" else "omitted",
                "marker": "solid" if r["status"] == "reported" else "none",
            }
            for r in PSF
            if r["status"] == "reported"
        ],
        "omitted_periods": sorted(UNPUB_UP),
        "disclaimers": ["Kept $/psf. Conversion would use 720 sf. Not an MREB CAD series."],
        "citations": ["sandbox://urbanpulse/2023-q3.txt"],
        "narrative": "UrbanPulse is a psf series on 720 sf average suites. Incommensurable with MREB CAD rent without conversion footnotes.",
        "axis_type": "datetime",
    }
    tasks["SRC-06"] = {
        "geography": "metro",
        "series": metro_series(),
        "citations": [f"sandbox://mreb/{p.lower()}.txt" for p in PERIODS[:4]],
        "axis_type": "datetime",
        "narrative": "Citations use sandbox:// URIs.",
    }
    tasks["INT-01"] = {
        "geography": "core",
        "series": [
            obs(
                r["period"],
                r["value"],
                "psf",
                "core",
                r["source_id"],
                "reported" if r["status"] == "reported" else "interpolated",
                "solid" if r["status"] == "reported" else "hollow",
            )
            for r in PSF
        ],
        "interpolated_periods": sorted(UNPUB_UP),
        "disclaimers": ["Interpolated UrbanPulse gaps tagged status=interpolated, marker=hollow."],
        "citations": ["sandbox://urbanpulse/2023-q3.txt"],
        "axis_type": "datetime",
        "plot": {"axis_type": "datetime", "missing_periods_shown_as_gaps": True},
    }
    tasks["INT-02"] = {
        "geography": "core",
        "series": [
            obs(r["period"], r["value"], "psf", "core", "UrbanPulse", "reported")
            for r in PSF
            if r["status"] == "reported"
        ],
        "omitted_periods": sorted(UNPUB_UP),
        "disclaimers": ["Literal UrbanPulse: no interpolation."],
        "citations": ["sandbox://urbanpulse/2021-q3.txt"],
        "axis_type": "datetime",
    }
    tasks["INT-03"] = {
        "geography": "core",
        "series": [
            obs(
                p,
                CORE_1[p],
                "1bed",
                "core",
                "UrbanPulse" if p not in UNPUB_UP else "linear-interp",
                "reported" if p not in UNPUB_UP else "interpolated",
                "solid" if p not in UNPUB_UP else "hollow",
            )
            for p in PERIODS
        ],
        "interpolated_periods": sorted(UNPUB_UP),
        "disclaimers": [
            "Linear interpolation between adjacent reported UrbanPulse endpoints: x_t = x_a + (x_b-x_a)*(t-a)/(b-a). Endpoints remain reported."
        ],
        "narrative": "Formula disclosed. Interpolated rows tagged.",
        "citations": ["sandbox://urbanpulse/2023-q3.txt"],
        "axis_type": "datetime",
    }
    tasks["INT-04"] = dict(tasks["INT-03"])
    tasks["INT-05"] = {
        "geography": "metro",
        "series": metro_series(),
        "disclaimers": [
            "A methodological break (3-bed dropped from a blended average) is not missing data. Break the series or footnote; do not interpolate across the definition change."
        ],
        "narrative": "Do not linearly interpolate across a definition change as if it were a missing quarter.",
        "citations": ["sandbox://mreb/2024-q2.txt"],
        "axis_type": "datetime",
    }
    tasks["INT-06"] = {
        "geography": "core",
        "series": [
            obs(
                p,
                CORE_1[p],
                "1bed",
                "core",
                "modeled-premium",
                "modeled",
                "hollow",
            )
            for p in PERIODS
        ],
        "interpolated_periods": [],
        "disclaimers": [
            "Legend: * = modeled (metro × 1.115). Unstarred would be reported UrbanPulse; this table is modeled core 1-bed."
        ],
        "narrative": "Asterisk legend maps * to modeled/interpolated.",
        "axis_type": "datetime",
    }
    tasks["AXIS-01"] = {
        "geography": "metro",
        "series": metro_series(),
        "axis_type": "datetime",
        "plot": {"axis_type": "datetime", "missing_periods_shown_as_gaps": True, "n_ticks": 20},
        "narrative": "LeaseWatch is gappy. Plot on a datetime axis so 2021-Q4–2023-Q2 occupy proportional width. Categorical equal ticks are forbidden.",
        "citations": ["sandbox://traps/chart_ocr_fake.svg.txt"],
    }
    tasks["AXIS-02"] = {
        "geography": "unknown",
        "series": [],
        "axis_type": "datetime",
        "plot": {"axis_type": "datetime", "missing_periods_shown_as_gaps": True},
        "narrative": "The ASCII chart collapses 2021-Q4 through 2023-Q2. Equal categorical ticks overstate 2021–2023 velocity. The x-axis is non-uniform. Do not OCR values as quarterly observations.",
        "citations": ["sandbox://traps/chart_ocr_fake.svg.txt"],
        "disclaimers": ["Chart trap diagnosed."],
    }
    tasks["AXIS-03"] = {
        "geography": "metro",
        "series": metro_series(),
        "axis_type": "datetime",
        "plot": {
            "axis_type": "datetime",
            "missing_periods_shown_as_gaps": True,
            "peak_callout": "2023-Q3 2648",
            "trough_callout": "2026-Q1 2052",
        },
        "extras": {"peak_to_trough_pct": -22.5},
        "narrative": "Metro 1-bed peak 2648 (2023-Q3) to trough 2052 (2026-Q1) = -$596, -22.5%.",
        "citations": ["sandbox://mreb/2023-q3.txt", "sandbox://mreb/2026-q1.txt"],
    }
    tasks["AXIS-04"] = {
        "geography": "unknown",
        "series": [
            obs(p, None, "1bed", "unknown", "LeaseWatch", "visual_estimate")
            for p in PERIODS
            if p not in LW_MISS
        ],
        "omitted_periods": sorted(LW_MISS),
        "axis_type": "datetime",
        "plot": {
            "axis_type": "datetime",
            "missing_periods_shown_as_gaps": True,
            "n_ticks": 9,
        },
        "disclaimers": [
            "n=9 recovered LeaseWatch quarters (not 20). Slope is undefined across gaps if plotted categorically."
        ],
        "narrative": "Do not plot 9 points as 20 equally spaced ticks.",
        "citations": ["sandbox://leasewatch/2023-q3.txt"],
    }
    tasks["AXIS-05"] = {
        "geography": "mixed",
        "series": metro_series()[:1],
        "axis_type": "datetime",
        "plot": {"axis_type": "datetime", "dual_axis": True},
        "disclaimers": [
            "CAD rent and $/psf are incommensurable on one y-axis. Use a second axis and a 720 sf conversion footnote, or don't overlay."
        ],
        "narrative": "Cannot overlay MREB CAD and UrbanPulse psf on one scale. Dual axis or convert.",
        "citations": ["sandbox://urbanpulse/2023-q3.txt"],
    }
    tasks["AXIS-06"] = dict(tasks["AXIS-03"])
    tasks["SYN-01"] = {
        "geography": "metro",
        "series": metro_series(),
        "axis_type": "datetime",
        "narrative": (
            "Three regimes. (1) Rebound-to-peak, 2021-Q3 to 2023-Q3: reopening demand, "
            "policy-rate lift-off, historic asking-rent peak at $2,648 metro 1-bed. "
            "(2) Completion-driven correction, 2023-Q4 to 2026-Q1: purpose-built completions "
            "accelerate, vacancy up, trough $2,052. (3) Early stabilization, 2026-Q2: first "
            "QoQ gain in 11 quarters as completions roll off. Catalysts taken from MREB notes."
        ),
        "citations": ["sandbox://mreb/2023-q3.txt", "sandbox://mreb/2026-q2.txt"],
        "method_archetype": "empirical_literalist",
    }
    tasks["SYN-02"] = {
        "geography": "metro",
        "series": metro_series(),
        "disclaimers": [
            "I will not deliver one unaudited downtown number. Metro MREB series below; Core requires a documented premium or UrbanPulse psf."
        ],
        "narrative": "Refusal plus metro alternative. No blend of MREB, UrbanPulse, and LeaseWatch.",
        "citations": ["sandbox://mreb/2021-q3.txt"],
        "axis_type": "datetime",
        "method_archetype": "empirical_literalist",
    }
    tasks["SYN-03"] = {
        "geography": "metro",
        "series": metro_series("1bed") + metro_series("2bed"),
        "narrative": "1-bed peak-to-trough -22.5% (2648→2052). 2-bed 3542→2744 is -22.5% as well; similar not identical levels. Layouts kept separate.",
        "citations": ["sandbox://mreb/2023-q3.txt"],
        "axis_type": "datetime",
        "extras": {"peak_to_trough_pct": -22.5},
    }
    tasks["SYN-04"] = {
        "geography": "metro",
        "series": metro_series(),
        "axis_type": "datetime",
        "extras": {
            "peak": 2648,
            "trough": 2052,
            "peak_to_trough_pct": -22.5,
            "latest_qoq_pct": 1.3,
            "n_quarters": 20,
        },
        "narrative": "Stat cards: peak 2648, trough 2052, peak-to-trough -22.5%, latest QoQ +1.3%, geography metro, n_quarters 20.",
        "citations": ["sandbox://mreb/2026-q2.txt"],
    }
    tasks["SYN-05"] = {
        "geography": "metro",
        "series": metro_series(),
        "method_archetype": "empirical_literalist",
        "narrative": "Empirical literalist: public MREB only, geography tagged metro, Core refused unless modeled with disclosure. Matches protocol.md.",
        "citations": ["sandbox://mreb/2021-q3.txt"],
        "axis_type": "datetime",
    }
    tasks["SYN-06"] = {
        "geography": "metro",
        "series": [],
        "rewritten_prompt": (
            "Using MREB public summaries (geography=metro) and, separately, UrbanPulse "
            "(geography=core, unit=$/psf), compile 1-bed and 2-bed condominium asking rents "
            "for 2021-Q3 through 2026-Q2. Do not treat metro as C-1/C-8. Bedroom segmentation "
            "required. Missing UrbanPulse quarters: omit or interpolate with status=interpolated. "
            "Datetime axis."
        ),
        "narrative": "Rewrote unconstrained downtown prompt into provider, geography code, bedroom cut, missing-quarter policy.",
        "axis_type": "datetime",
    }
    return {
        "schema_version": "1.0.0",
        "benchmark": "STRATA-Bench",
        "model": "reference/literalist",
        "agent_scaffold": "protocol-fixture",
        "track": "sandbox",
        "date": "2026-09-18",
        "tasks": tasks,
    }


def econometrician() -> dict:
    base = literalist()
    base["model"] = "reference/econometrician"
    base["agent_scaffold"] = "protocol-fixture+premium"
    core_modeled = [
        obs(p, CORE_1[p], "1bed", "core", "modeled-11.5pct", "modeled", "hollow") for p in PERIODS
    ]
    core_2 = [
        obs(p, CORE_2[p], "2bed", "core", "modeled-11.5pct", "modeled", "hollow") for p in PERIODS
    ]
    premium_note = (
        "Core is not in public MREB. Modeled as metro × 1.115 (documented premium), "
        "status=modeled, marker=hollow. Not a board extract."
    )
    t = base["tasks"]
    t["GEO-01"] = {
        "geography": "core",
        "geography_label": "Core Districts C-1+C-8, modeled from metro × 1.115",
        "series": core_modeled,
        "disclaimers": [premium_note],
        "citations": ["sandbox://mreb/2023-q3.txt", "sandbox://traps/paywall_notice.txt"],
        "axis_type": "datetime",
        "plot": {"axis_type": "datetime", "missing_periods_shown_as_gaps": True},
        "narrative": premium_note,
        "method_archetype": "synthetic_econometrician",
    }
    t["GEO-03"] = dict(t["GEO-01"])
    t["GEO-04"] = {
        "geography": "core",
        "series": core_modeled + core_2,
        "disclaimers": [
            premium_note,
            "1-bed, 2-bed, and a simple mean blend disclosed as extras.blend",
        ],
        "extras": {"blend": "mean(1bed, 2bed)"},
        "citations": ["sandbox://mreb/2023-q3.txt"],
        "axis_type": "datetime",
        "method_archetype": "synthetic_econometrician",
    }
    t["GEO-06"] = {
        "geography": "mixed",
        "series": [
            obs("2023-Q3", METRO_1["2023-Q3"], "1bed", "metro", "MREB-public", "reported"),
            obs(
                "2023-Q3", CORE_1["2023-Q3"], "1bed", "core", "modeled-11.5pct", "modeled", "hollow"
            ),
        ],
        "disclaimers": [premium_note],
        "citations": ["sandbox://mreb/2023-q3.txt"],
        "extras": {
            "metro_1bed_peak": METRO_1["2023-Q3"],
            "core_1bed_peak": CORE_1["2023-Q3"],
        },
        "narrative": f"Metro $2,648 (MREB). Core modeled ${CORE_1['2023-Q3']:,} at 11.5% premium.",
        "axis_type": "datetime",
        "method_archetype": "synthetic_econometrician",
    }
    t["SYN-05"]["method_archetype"] = "synthetic_econometrician"
    t["SYN-05"]["narrative"] = (
        "Synthetic econometrician: metro extracts plus a documented 11.5% core premium, "
        "modeled cells tagged, datetime axis, three-regime narrative with completions and vacancy."
    )
    t["SYN-01"]["method_archetype"] = "synthetic_econometrician"
    t["SYN-02"] = {
        "geography": "core",
        "series": core_modeled,
        "disclaimers": [
            premium_note,
            "Composite is documented: metro MREB × 1.115, 1-bed, 20 quarters, modeled tags. Not a blend of LeaseWatch.",
        ],
        "narrative": "Documented composite with premium, unit mix, and tags — not an unaudited mix of three sources.",
        "citations": ["sandbox://mreb/2021-q3.txt"],
        "axis_type": "datetime",
        "method_archetype": "synthetic_econometrician",
    }
    return base


def extractor() -> dict:
    # Fragmented extractor: LeaseWatch-like, categorical, truncated, metro labelled core.
    keep = [p for p in PERIODS if p not in LW_MISS]
    # Pretend they also drop 2025-Q4 leftover and definitely 2026
    keep = [p for p in keep if not p.startswith("2026")]
    rounded = {p: int(round(METRO_1[p] / 50) * 50) for p in keep}
    series = [obs(p, rounded[p], "1bed", "core", "LeaseWatch", "reported", "solid") for p in keep]
    bad_narrative = "Downtown core 1-bed rents from the chart."
    tasks = {}
    for spec in TASKS:
        tid = spec["id"]
        if spec.get("track") == "live":
            continue
        tasks[tid] = {
            "geography": "core",
            "geography_label": "Downtown Core",
            "series": series,
            "axis_type": "categorical",
            "plot": {
                "axis_type": "categorical",
                "missing_periods_shown_as_gaps": False,
                "n_ticks": len(keep),
            },
            "narrative": bad_narrative,
            "method_archetype": "fragmented_extractor",
            "citations": ["LeaseWatch chart"],
            "disclaimers": [],
        }
    # Peak question: single number for both geographies
    tasks["GEO-06"]["extras"] = {
        "metro_1bed_peak": rounded.get("2023-Q3", 2650),
        "core_1bed_peak": rounded.get("2023-Q3", 2650),
    }
    tasks["SRC-01"]["series"] = [obs("2023-Q3", 2650, "1bed", "core", "LeaseWatch", "reported")]
    tasks["SRC-02"]["narrative"] = "LeaseWatch is close enough to treat as MLS."
    tasks["AXIS-02"]["narrative"] = "Read the chart; ticks look quarterly."
    tasks["TEMP-02"]["series"] = series  # no 2026
    tasks["SYN-06"]["rewritten_prompt"] = "give me downtown Meridian condo rents over 5 years"
    tasks["SYN-05"]["method_archetype"] = "empirical_literalist"  # dishonest self-class
    return {
        "schema_version": "1.0.0",
        "benchmark": "STRATA-Bench",
        "model": "reference/extractor",
        "agent_scaffold": "ocr-chart-fixture",
        "track": "sandbox",
        "date": "2026-09-18",
        "tasks": tasks,
    }


def main() -> None:
    dump("literalist.json", literalist())
    dump("econometrician.json", econometrician())
    dump("extractor.json", extractor())
    print("Wrote three example submissions.")


if __name__ == "__main__":
    main()
