"""Human-readable scorecards."""

from __future__ import annotations

from typing import Any

from .schema import DIMENSIONS

DIM_LABEL = {
    "temporal_coverage": "Temporal coverage",
    "source_grounding": "Source grounding",
    "spatial_precision": "Spatial precision",
    "statistical_rigor": "Statistical rigor",
    "visual_integrity": "Visual / axis integrity",
    "macro_narrative": "Macro narrative",
}


def _bar(score: float, width: int = 20) -> str:
    filled = round(score / 10 * width)
    return "█" * filled + "░" * (width - filled)


def render_text(result: dict[str, Any]) -> str:
    lines = [
        "STRATA-Bench  v{version}".format(**result),
        f"Model     {result['model']}",
        f"Scaffold  {result.get('agent_scaffold') or '—'}",
        f"Track     {result['track']}",
        "",
        f"Headline score   {result['headline_score']:>6.2f} / 10",
        f"Task-weighted    {result['task_weighted_score']:>6.2f} / 10",
        f"Answered         {result['n_answered']}/{result['n_tasks']}",
        f"Hard fails       {result['n_hard_fails']}",
        "",
        "Dimensions",
    ]
    for k in DIMENSIONS:
        v = result["dimension_scores"][k]
        lines.append(f"  {DIM_LABEL[k]:<28} {v:5.2f}  {_bar(v)}")
    if result["hard_fails"]:
        lines.append("\nHard-fail codes: " + ", ".join(result["hard_fails"]))
    lines.append("\nPer-task composites")
    for t in result["tasks"]:
        flag = "  FAIL " if t["hard_fails"] else "       "
        lines.append(f"  {t['id']:<9}{t['composite']:5.2f}{flag}{', '.join(t['hard_fails'])}")
    lines.append("")
    return "\n".join(lines)


def render_markdown(result: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {DIM_LABEL[k]} | {result['dimension_scores'][k]:.2f} |" for k in DIMENSIONS
    )
    task_rows = "\n".join(
        f"| {t['id']} | {t['composite']:.2f} | {', '.join(t['hard_fails']) or '—'} |"
        for t in result["tasks"]
    )
    return f"""# STRATA-Bench scorecard

**Model:** {result["model"]}  
**Scaffold:** {result.get("agent_scaffold") or "—"}  
**Track:** `{result["track"]}`  
**Headline:** **{result["headline_score"]:.2f} / 10**

## Dimensions

| Dimension | Score |
| --- | ---: |
{rows}

## Tasks

| Task | Composite | Hard fails |
| --- | ---: | --- |
{task_rows}
"""
