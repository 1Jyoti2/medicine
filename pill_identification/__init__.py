"""
Pill Identification Package.
Production-ready visual recognition of pharmaceutical pills and NDC metadata mapping.
"""

from .predictor import (
    PillClassifier,
    get_pill_classifier,
    load_pill_classifier,
    PillInferenceError,
)
from .preprocessing import (
    PillPreprocessor,
    get_preprocessor,
    PillImageError,
    InvalidPillImageError,
    CorruptedPillImageError,
)
from .schemas import (
    PillCandidate,
    PillInferenceResult,
)

__all__ = [
    "PillClassifier",
    "get_pill_classifier",
    "load_pill_classifier",
    "PillPreprocessor",
    "get_preprocessor",
    "PillCandidate",
    "PillInferenceResult",
    "PillInferenceError",
    "PillImageError",
    "InvalidPillImageError",
    "CorruptedPillImageError",
]

__version__ = "1.0.0"
