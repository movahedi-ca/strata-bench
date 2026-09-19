# Contributing to STRATA-Bench

Thank you. The benchmark is only useful if gold, prompts, and the scorer stay aligned.

## Ground rules

1. **Do not fix a task by leaking gold into the prompt.** If agents fail GEO-01, tighten the success condition or the scorer — do not print `$2,953` in the user-facing prompt.
2. **Bump the version** in `pyproject.toml`, `CITATION.cff`, and `strata_bench/__init__.py` when gold or scoring changes. Additive tasks may be `1.0.x`.
3. **Keep Track Sandbox offline.** No new task may require the public internet.
4. Run `python scripts/generate_sandbox.py && pytest -q` before opening a PR.

## Adding a task

- Add a dict to `TASKS` in `scripts/generate_sandbox.py` with `id`, `family`, `title`, `prompt`, `success`, `hard_fail`, `primary_dimension`, `weight`, `gold_keys`.
- Regenerate. Add a fixture assertion in `tests/test_examples.py` if the task should split the three archetypes.
- Document it in `docs/tasks.md`.

## Code style

Python 3.10+, Ruff, Pytest. No extra runtime deps beyond Pydantic.

## Leaderboard submissions

Open an issue with the **Evaluation run** template and attach the `strata-bench evaluate --format json` output. Maintainers will not accept scores without the submission JSON.
