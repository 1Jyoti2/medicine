"""
Pill Identification Schemas.
"""

from typing import List, Optional, Any
from pydantic import BaseModel


class PillCandidate(BaseModel):
    name: str
    genericName: str
    strength: str
    ndcCode: Optional[str] = None
    confidence: float
    confidence_percent: str


class MedicineProfile(BaseModel):
    id: str
    name: str
    genericName: str
    category: Optional[str] = "Prescription Medication"
    composition: Optional[str] = None
    manufacturer: Optional[str] = "FDA Registered"
    dosage: Optional[str] = None
    storage: Optional[str] = None
    uses: List[str] = []
    sideEffects: List[str] = []
    precautions: List[str] = []
    description: Optional[str] = None


class PillPredictionResult(BaseModel):
    id: str
    medicine: MedicineProfile
    confidence: float
    confidence_percent: str
    topPredictions: List[PillCandidate]
    ndcCode: Optional[str] = None
    imageName: str
    analyzedAt: str
    model: str = "mobilenet_v2"
    status: str = "success"
    inferenceTimeMs: float = 0.0
