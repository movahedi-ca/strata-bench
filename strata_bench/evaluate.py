"""Evaluate a STRATA-Bench JSON submission against hidden gold."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schema import DIMENSIONS, DIMENSION_WEIGHTS, Submission, TaskAnswer
from .scoring import Scorecard, score_task

PKG_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLD = PKG_ROOT / "data" / "hidden" / "gold.json"
DEFAULT_TASKS = PKG_ROOT / "data" / "public" / "tasks.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_gold(path: Path | None = None) -> dict[str, Any]:
    return load_json(path or DEFAULT_GOLD)


def load_tasks(path: Path | None = None) -> dict[str, Any]:
    return load_json(path or DEFAULT_TASKS)


def _weighted_mean(cards: list[Scorecard], tasks_by_id: dict[str, dict]) -> float:
    num = 0.0
    den = 0.0
    for c in cards:
        w = float(tasks_by_id.get(c.task_id, {}).get("weight", 1.0))
        num += c.composite * w
        den += w
    return round(num / den, 2) if den else 0.0


def _dimension_means(cards: list[Scorecard]) -> dict[str, float]:
    if not cards:
        return {k: 0.0 for k in DIMENSIONS}
    return {
        k: round(sum(getattr(c.scores, k) for c in cards) / len(cards), 2) for k in DIMENSIONS
    }


def evaluate_submission(
    submission: Submission | dict[str, Any] | Path,
    gold: dict[str, Any] | None = None,
    catalog: dict[str, Any] | None = None,
    track: str | None = None,
) -> dict[str, Any]:
    if isinstance(submission, Path):
        submission = Submission.model_validate(load_json(submission))
    elif isinstance(submission, dict):
        submission = Submission.model_validate(submission)
    gold = gold or load_gold()
    catalog = catalog or load_tasks()
    track = track or submission.track

    allowed = set(catalog["tracks"].get(track, catalog["tracks"]["sandbox"]))
    tasks_by_id = {t["id"]: t for t in catalog["tasks"] if t["id"] in allowed}

    cards: list[Scorecard] = []
    missing: list[str] = []
    for task_id, task in tasks_by_id.items():
        answer = submission.tasks.get(task_id)
        if answer is None:
            missing.append(task_id)
            card = score_task(task, TaskAnswer(), gold)
            card.notes.append("Task not answered.")
            cards.append(card)
        else:
            cards.append(score_task(task, answer, gold))

    composite = _weighted_mean(cards, tasks_by_id)
    dim = _dimension_means(cards)
    official = sum(dim[k] * w for k, w in DIMENSION_WEIGHTS.items())
    headline = round(0.7 * composite + 0.3 * official, 2)

    hard = sorted({code for c in cards for code in c.hard_fails})
    return {
        "benchmark": "STRATA-Bench",
        "version": "1.0.0",
        "model": submission.model,
        "agent_scaffold": submission.agent_scaffold,
        "track": track,
        "headline_score": headline,
        "task_weighted_score": composite,
        "dimension_scores": dim,
        "n_tasks": len(cards),
        "n_answered": len(cards) - len(missing),
        "n_missing": len(missing),
        "missing_tasks": missing,
        "hard_fails": hard,
        "n_hard_fails": sum(len(c.hard_fails) for c in cards),
        "tasks": [
            {
                "id": c.task_id,
                "composite": c.composite,
                "scores": c.scores.as_dict(),
                "hard_fails": c.hard_fails,
                "notes": c.notes,
                "n_matched": c.n_matched,
                "n_expected": c.n_expected,
            }
            for c in cards
        ],
    }
