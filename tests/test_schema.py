from strata_bench.schema import DIMENSION_WEIGHTS, PERIODS, Submission


def test_weights_sum_to_one():
    assert abs(sum(DIMENSION_WEIGHTS.values()) - 1.0) < 1e-9


def test_twenty_quarters():
    assert len(PERIODS) == 20
    assert PERIODS[0] == "2021-Q3"
    assert PERIODS[-1] == "2026-Q2"


def test_submission_parses_minimal():
    s = Submission.model_validate({"model": "x", "tasks": {}})
    assert s.track == "sandbox"
    assert s.schema_version == "1.0.0"
