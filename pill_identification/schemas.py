"""
Schemas and data structures for Pill Identification and Metadata Lookup.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


@dataclass
class PillCandidate:
    """Individual candidate prediction for a pill image."""
    rank: int
    class_name: str
    drug_name: str
    generic_name: str
    strength: str
    dosage_form: str
    ndc_code: Optional[str]
    confidence: float
    confidence_percent: str
    manufacturer: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PillInferenceResult:
    """Full inference result returned by the Pill Identification service."""
    success: bool
    predicted_class: str
    predicted_drug: str
    generic_name: str
    strength: str
    dosage_form: str
    ndc_code: Optional[str]
    confidence: float
    confidence_percent: str
    top_predictions: List[PillCandidate] = field(default_factory=list)
    manufacturer: Optional[str] = None
    description: Optional[str] = None
    inference_time_ms: float = 0.0
    image_path: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
