"""Dimension scoring and hard-fail detection for a single STRATA task."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .schema import (
    DIMENSIONS,
    HARD_FAIL_CODES,
    PERIODS,
    TaskAnswer,
)

TOLERANCE = 0.015  # 1.5% relative error on numeric cells
ABS_TOL = 8.0  # dollars


@dataclass
class DimensionScores:
    temporal_coverage: float = 0.0
    source_grounding: float = 0.0
    spatial_precision: float = 0.0
    statistical_rigor: float = 0.0
    visual_integrity: float = 0.0
    macro_narrative: float = 0.0

    def as_dict(self) -> dict[str, float]:
        return {k: round(getattr(self, k), 2) for k in DIMENSIONS}


@dataclass
class Scorecard:
    task_id: str
    scores: DimensionScores
    hard_fails: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    n_matched: int = 0
    n_expected: int = 0

    @property
    def composite(self) -> float:
        from .schema import DIMENSION_WEIGHTS

        raw = sum(getattr(self.scores, k) * w for k, w in DIMENSION_WEIGHTS.items())
        if self.hard_fails:
            raw *= 0.55
        return round(raw, 2)


def _periods(answer: TaskAnswer) -> list[str]:
    return [o.period for o in answer.series]


def _text(answer: TaskAnswer) -> str:
    parts = [
        answer.narrative or "",
        answer.geography_label or "",
        answer.rewritten_prompt or "",
        " ".join(answer.disclaimers),
        " ".join(answer.citations),
        " ".join(answer.omitted_periods),
        " ".join(answer.interpolated_periods),
    ]
    return " ".join(parts).lower()


def _gold_map(gold: dict[str, Any], key: str) -> dict[str, float]:
    rows = gold.get("series", {}).get(key, [])
    return {r["period"]: float(r["value"]) for r in rows if r.get("value") is not None}


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= max(ABS_TOL, TOLERANCE * abs(b))


def _coverage_score(answer: TaskAnswer, expected: list[str] | None = None) -> float:
    expected = expected or PERIODS
    got = set(_periods(answer)) | set(answer.omitted_periods)
    if not expected:
        return 5.0
    hit = sum(1 for p in expected if p in got)
    ratio = hit / len(expected)
    honesty = 1.0 if (set(expected) - set(_periods(answer))) <= listed_or_empty(answer) else 0.85
    return round(min(10.0, 10.0 * ratio * honesty), 2)


def listed_or_empty(answer: TaskAnswer) -> set[str]:
    return set(answer.omitted_periods) | set(answer.interpolated_periods)


def _source_score(answer: TaskAnswer, task: dict[str, Any]) -> tuple[float, list[str]]:
    fails: list[str] = []
    text = _text(answer)
    n = len(answer.series)
    cited = sum(1 for o in answer.series if o.source_id)
    cite_ratio = 1.0 if n == 0 else cited / n
    score = 8.0 * cite_ratio
    if answer.citations:
        score += 1.0
    cites = " ".join(answer.citations).lower()
    if "sandbox://" in cites or "mreb" in cites:
        score += 0.5
    silent = [
        o
        for o in answer.series
        if o.status == "reported" and o.period in answer.interpolated_periods
    ]
    if silent:
        fails.append("SILENT_INTERP")
        score = min(score, 3.0)
    if task["id"] == "SRC-02" and "not" not in text and "leasewatch" in text:
        fails.append("OCR_LAUNDER")
        score = min(score, 3.0)
    if task["id"] == "SRC-01" and any(
        o.source_id and "lease" in o.source_id.lower() for o in answer.series
    ):
        fails.append("OCR_LAUNDER")
        score = min(score, 3.0)
    if task["id"] == "GEO-05" and any(
        o.geography == "core"
        and o.status == "reported"
        and o.source_id
        and "mreb" in o.source_id.lower()
        for o in answer.series
    ):
        fails.append("HALLUCINATED_PAYWALL")
        score = min(score, 2.0)
    return round(min(10.0, score), 2), fails


def _value_at(answer: TaskAnswer, period: str, geography: str | None = None) -> float | None:
    for o in answer.series:
        if o.period == period and o.value is not None:
            if geography is None or o.geography == geography:
                return o.value
    return None


def _spatial_score(
    answer: TaskAnswer, task: dict[str, Any], gold: dict[str, Any]
) -> tuple[float, list[str]]:
    fails: list[str] = []
    text = _text(answer)
    labels = (answer.geography_label or "").lower()
    geo = answer.geography
    score = 7.0

    metro_as_core = False
    if geo == "core" or "downtown" in labels or "core" in labels:
        metro_vals = _gold_map(gold, "metro_1bed")
        for o in answer.series:
            if o.value is None or o.period not in metro_vals:
                continue
            if _close(o.value, metro_vals[o.period]) and o.geography in {"core", "unknown"}:
                if o.status == "reported" and not answer.disclaimers:
                    metro_as_core = True
    if metro_as_core and task["family"] == "GEO":
        fails.append("GEO_MASK")
        score = 1.5
    else:
        tagged = sum(1 for o in answer.series if o.geography in {"metro", "core"})
        n = len(answer.series)
        if n:
            score = 4.0 + 6.0 * (tagged / n)
        if geo == "metro" and "not" in text and "core" in text:
            score = max(score, 9.0)
        if answer.disclaimers and ("premium" in text or "metro" in text):
            score = min(10.0, score + 1.0)
        if task["id"] == "GEO-06":
            extras = answer.extras or {}
            m = extras.get("metro_1bed_peak") or _value_at(answer, "2023-Q3", "metro")
            c = extras.get("core_1bed_peak") or _value_at(answer, "2023-Q3", "core")
            if m and c and abs(float(c) - float(m)) < 20:
                fails.append("GEO_MASK")
                score = min(score, 3.0)
            elif m and _close(float(m), gold["milestones"]["2023-Q3"]["metro_1bed"]):
                score = max(score, 8.5)
    return round(min(10.0, score), 2), fails


def _stat_score(
    answer: TaskAnswer, task: dict[str, Any], gold: dict[str, Any]
) -> tuple[float, list[str], int, int]:
    fails: list[str] = []
    score = 6.0
    text = _text(answer)
    key = (task.get("gold_keys") or ["metro_1bed"])[0]
    gmap = _gold_map(gold, key) if key else {}
    matched = 0
    expected = 0
    for o in answer.series:
        if o.period in gmap and o.value is not None:
            if o.geography == "core" and key.startswith("metro"):
                continue
            expected += 1
            if _close(o.value, gmap[o.period]):
                matched += 1
    if expected:
        score = 10.0 * matched / expected
    if task["id"] == "AXIS-03":
        if "22.5" in text or (answer.extras or {}).get("peak_to_trough_pct") is not None:
            extras = answer.extras or {}
            if extras.get("peak_to_trough_pct") is not None and abs(
                float(extras["peak_to_trough_pct"]) - (-22.5)
            ) < 0.6:
                score = 10.0
            elif "22.5" in text:
                score = max(score, 9.5)
    if task["id"] == "SRC-05" and "psf" not in text and not any(o.unit == "psf" for o in answer.series):
        fails.append("UNIT_COLLAPSE")
        score = min(score, 4.0)
    if task["id"] == "SYN-02" and len(answer.series) <= 1 and not answer.disclaimers:
        fails.append("BLEND")
        score = min(score, 4.0)
    return round(min(10.0, score), 2), fails, matched, expected


def _visual_score(answer: TaskAnswer, task: dict[str, Any]) -> tuple[float, list[str]]:
    fails: list[str] = []
    score = 5.0
    axis = answer.axis_type
    if answer.plot:
        axis = answer.plot.axis_type or axis
    text = _text(answer)
    if axis == "datetime":
        score = 9.0
        if answer.plot and answer.plot.missing_periods_shown_as_gaps:
            score = 10.0
    elif axis == "categorical":
        gappy = len(answer.series) < 16 or bool(answer.omitted_periods)
        if gappy and task["family"] in {"AXIS", "TEMP", "INT", "GEO", "SRC", "SYN"}:
            fails.append("CATEGORICAL_GAP")
            score = 2.0
        else:
            score = 4.0
    if "gap" in text and "datetime" in text:
        score = max(score, 8.5)
    if task["id"] == "INT-04":
        n = len(answer.series)
        marked = sum(1 for o in answer.series if o.marker in {"solid", "hollow"})
        score = 10.0 * marked / n if n else 3.0
    if task["id"] == "AXIS-02" and (
        "collapsed" in text or "non-uniform" in text or "gap" in text
    ):
        score = max(score, 9.0)
    if task["id"] == "AXIS-05" and (
        "incommensur" in text or "second axis" in text or "dual" in text or "cannot" in text
    ):
        score = max(score, 9.0)
    return round(min(10.0, score), 2), fails


def _macro_score(answer: TaskAnswer, task: dict[str, Any]) -> float:
    text = _text(answer)
    if task["family"] not in {"SYN", "LIVE"} and not answer.narrative:
        return 6.0
    hits = 0
    for token in (
        "peak",
        "trough",
        "completion",
        "vacancy",
        "rebound",
        "premium",
        "2023-q3",
        "2026-q1",
        "regime",
        "interpolat",
        "metro",
        "core",
        "mreb",
        "datetime",
        "c-1",
        "geography",
    ):
        if token in text:
            hits += 1
    score = min(10.0, 4.0 + hits * 0.6)
    if task["id"] == "SYN-06":
        need = ["mreb", "bedroom", "quarter", "geograph"]
        score = 2.5 * sum(1 for t in need if t in text)
    if task["id"] == "SYN-05" and answer.method_archetype:
        score = max(score, 8.0)
        if (
            answer.method_archetype == "empirical_literalist"
            and answer.geography == "core"
            and not answer.disclaimers
        ):
            score = min(score, 4.0)
    return round(min(10.0, score), 2)


def score_task(task: dict[str, Any], answer: TaskAnswer, gold: dict[str, Any]) -> Scorecard:
    notes: list[str] = []
    fails: list[str] = []

    empty = (
        not answer.series
        and not (answer.narrative or "").strip()
        and not answer.disclaimers
        and not answer.citations
        and not answer.rewritten_prompt
        and not answer.omitted_periods
        and not answer.interpolated_periods
    )
    if empty:
        return Scorecard(
            task_id=task["id"],
            scores=DimensionScores(
                temporal_coverage=1.0,
                source_grounding=1.0,
                spatial_precision=1.0,
                statistical_rigor=1.0,
                visual_integrity=1.0,
                macro_narrative=1.0,
            ),
            notes=["Empty answer."],
        )

    temporal = _coverage_score(answer)
    if task["id"] == "TEMP-02":
        got = set(_periods(answer))
        if "2026-Q1" not in got or "2026-Q2" not in got:
            fails.append("TRUNCATE_2026")
            temporal = min(temporal, 4.0)
        else:
            v1 = _value_at(answer, "2026-Q1", "metro") or _value_at(answer, "2026-Q1")
            v2 = _value_at(answer, "2026-Q2", "metro") or _value_at(answer, "2026-Q2")
            if v1 and v2 and v2 > v1:
                temporal = max(temporal, 9.5)

    source, f1 = _source_score(answer, task)
    spatial, f2 = _spatial_score(answer, task, gold)
    stat, f3, matched, expected = _stat_score(answer, task, gold)
    visual, f4 = _visual_score(answer, task)
    macro = _macro_score(answer, task)

    for code in f1 + f2 + f3 + f4:
        if code not in fails:
            fails.append(code)
            notes.append(HARD_FAIL_CODES.get(code, code))

    scores = DimensionScores(
        temporal_coverage=temporal,
        source_grounding=source,
        spatial_precision=spatial,
        statistical_rigor=stat,
        visual_integrity=visual,
        macro_narrative=macro,
    )
    primary = task.get("primary_dimension")
    if primary and getattr(scores, primary) < 3 and not fails:
        notes.append(f"Low primary dimension ({primary}).")

    return Scorecard(
        task_id=task["id"],
        scores=scores,
        hard_fails=fails,
        notes=notes,
        n_matched=matched,
        n_expected=expected,
    )
