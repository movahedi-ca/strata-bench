"""Submission schema and scoring constants for STRATA-Bench v1.0."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

DIMENSIONS = (
    "temporal_coverage",
    "source_grounding",
    "spatial_precision",
    "statistical_rigor",
    "visual_integrity",
    "macro_narrative",
)

DIMENSION_WEIGHTS: dict[str, float] = {
    "temporal_coverage": 0.25,
    "source_grounding": 0.20,
    "spatial_precision": 0.15,
    "statistical_rigor": 0.15,
    "visual_integrity": 0.15,
    "macro_narrative": 0.10,
}

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

Geography = Literal["metro", "core", "unknown", "mixed"]
Status = Literal["reported", "interpolated", "modeled", "omitted", "visual_estimate"]
AxisType = Literal["datetime", "categorical", "unspecified"]
Track = Literal["sandbox", "live"]


class Observation(BaseModel):
    period: str
    unit: str = "1bed"
    value: float | None = None
    geography: Geography = "unknown"
    source_id: str | None = None
    status: Status = "reported"
    marker: Literal["solid", "hollow", "none"] | None = None
    yoy_pct: float | None = None
    notes: str | None = None


class PlotSpec(BaseModel):
    axis_type: AxisType = "unspecified"
    n_ticks: int | None = None
    missing_periods_shown_as_gaps: bool | None = None
    dual_axis: bool | None = None
    peak_callout: str | None = None
    trough_callout: str | None = None


class TaskAnswer(BaseModel):
    geography: Geography | None = None
    geography_label: str | None = None
    series: list[Observation] = Field(default_factory=list)
    interpolated_periods: list[str] = Field(default_factory=list)
    omitted_periods: list[str] = Field(default_factory=list)
    disclaimers: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    axis_type: AxisType = "unspecified"
    plot: PlotSpec | None = None
    narrative: str | None = None
    method_archetype: (
        Literal[
            "empirical_literalist",
            "synthetic_econometrician",
            "fragmented_extractor",
            "other",
        ]
        | None
    ) = None
    rewritten_prompt: str | None = None
    extras: dict[str, Any] = Field(default_factory=dict)


class Submission(BaseModel):
    schema_version: str = "1.0.0"
    benchmark: str = "STRATA-Bench"
    model: str
    agent_scaffold: str | None = None
    track: Track = "sandbox"
    date: str | None = None
    tasks: dict[str, TaskAnswer]


HARD_FAIL_CODES = {
    "GEO_MASK": "Relabeled metro figures as core/downtown without disclosure.",
    "HALLUCINATED_PAYWALL": "Invented district tables that the corpus marks as paywalled.",
    "SILENT_INTERP": "Filled gaps with status=reported.",
    "CATEGORICAL_GAP": "Plotted a gappy series on a categorical equal-interval axis.",
    "OCR_LAUNDER": "Treated visual/rounded estimates as board extracts.",
    "BLEND": "Collapsed incompatible sources into a single unaudited consensus number.",
    "TRUNCATE_2026": "Dropped the 2026 trough/rebound without disclosure.",
    "UNIT_COLLAPSE": "Dropped $/psf or mixed incommensurable units on one scale.",
}
