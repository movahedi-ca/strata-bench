# Changelog

All notable changes to STRATA-Bench are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The **benchmark itself** — sandbox corpus, task catalog, scorer, and gold —
is frozen at v1.0.0. Later releases change tooling, docs, and packaging only,
unless explicitly noted.

## [1.1.0] — 2026-09-19

### Added
- Community leaderboard: open a PR adding `submissions/community/<name>.json`
  and a GitHub Action scores it and posts the scorecard as a PR comment.
- GitHub Pages documentation site served from `docs/`
  (`https://movahedi-ca.github.io/strata-bench/`).
- Automated PyPI publishing via trusted publishing on GitHub releases.
- `python -m strata_bench` entry point.
- Coverage reporting in CI (Codecov) and a coverage badge.
- `dependabot.yml` for pip and GitHub Actions updates.
- Pull request template.
- `scripts/` are now executable and the codebase is `ruff check` / `ruff format` clean.

### Changed
- CI now runs lint (ruff), tests across Python 3.10–3.12 with pip caching,
  a CLI smoke test, and coverage upload.
- README: hero image, community leaderboard section, docs-site links.

## [1.0.0] — 2026-09-19

### Added
- Initial public release: 36 sandbox tasks + 3 live probes, evaluation
  harness (`strata-bench` CLI + Python API), three reference agents,
  protocol/scoring/prompting docs, and CI.
