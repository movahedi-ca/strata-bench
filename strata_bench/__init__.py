"""STRATA-Bench: Spatial-Temporal Retrieval, Alignment, Transparency & Audit."""

from .evaluate import evaluate_submission, load_gold, load_tasks
from .schema import DIMENSIONS, DIMENSION_WEIGHTS, Submission
from .scoring import Scorecard, score_task

__version__ = "1.0.0"
__all__ = [
    "DIMENSIONS",
    "DIMENSION_WEIGHTS",
    "Scorecard",
    "Submission",
    "evaluate_submission",
    "load_gold",
    "load_tasks",
    "score_task",
    "__version__",
]
