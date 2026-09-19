"""Regression tests: the three archetypes must separate cleanly."""

from __future__ import annotations

from pathlib import Path

from strata_bench import evaluate_submission

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "submissions" / "examples"


def _run(name: str) -> dict:
    return evaluate_submission(EX / name)


def test_literalist_is_strong_and_clean():
    r = _run("literalist.json")
    assert r["n_missing"] == 0
    assert r["headline_score"] >= 7.5
    assert "GEO_MASK" not in r["hard_fails"]
    assert "TRUNCATE_2026" not in r["hard_fails"]
    assert "CATEGORICAL_GAP" not in r["hard_fails"]


def test_econometrician_is_strong():
    r = _run("econometrician.json")
    assert r["headline_score"] >= 7.5
    assert "GEO_MASK" not in r["hard_fails"]
    geo06 = next(t for t in r["tasks"] if t["id"] == "GEO-06")
    assert geo06["composite"] >= 5.0


def test_extractor_is_weak_and_dirty():
    r = _run("extractor.json")
    assert r["headline_score"] < 5.5
    assert r["n_hard_fails"] >= 3
    assert "GEO_MASK" in r["hard_fails"] or "CATEGORICAL_GAP" in r["hard_fails"]
    assert "TRUNCATE_2026" in r["hard_fails"]


def test_ordering():
    lit = _run("literalist.json")["headline_score"]
    eco = _run("econometrician.json")["headline_score"]
    ext = _run("extractor.json")["headline_score"]
    assert min(lit, eco) - ext >= 2.0


def test_empty_submission_does_not_crash():
    r = evaluate_submission(
        {
            "model": "none",
            "track": "sandbox",
            "tasks": {},
        }
    )
    assert r["n_answered"] == 0
    assert r["headline_score"] < 4.0
