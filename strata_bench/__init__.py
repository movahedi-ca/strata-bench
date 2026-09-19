"""STRATA-Bench: Spatial-Temporal Retrieval, Alignment, Transparency & Audit."""

from .evaluate import evaluate_submission, load_gold, load_tasks
from .schema import DIMENSION_WEIGHTS, DIMENSIONS, Submission
from .scoring import Scorecard, score_task

__version__ = "1.1.0"
__all__ = [
    "DIMENSIONS",
    "DIMENSION_WEIGHTS",
    "Scorecard",
    "Submission",
    "__version__",
    "evaluate_submission",
    "load_gold",
    "load_tasks",
    "score_task",
]
