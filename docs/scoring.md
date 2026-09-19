# Scoring

## Headline

```
headline = 0.7 · task_weighted + 0.3 · dimension_mean

task_weighted = Σ (task.composite × task.weight) / Σ task.weight

dimension_mean = 0.25·temporal + 0.20·source + 0.15·spatial
               + 0.15·statistical + 0.15·visual + 0.10·narrative
```

Each dimension is 0–10. Each task composite uses the same weights, then ×0.55 if the task incurred any hard fail.

## Numeric match

On series tasks, a cell matches gold if

```
|v - gold| ≤ max(8 CAD, 1.5% · |gold|)
```

Core cells are matched against `core_*` gold (metro × 1.115, nearest dollar). Metro cells against `metro_*`.

## What is *not* scored

Prose quality beyond keyword coverage of catalysts, chart pixel polish, and brand voice. A correct, ugly table beats a beautiful, masked one.

## Reproducibility

`strata-bench evaluate` is deterministic. Seed example scores are CI fixtures. If you change gold or the scorer, bump the version in `pyproject.toml` and `CITATION.cff`.
