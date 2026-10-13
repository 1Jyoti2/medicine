"""
Leaf Prediction Request & Response Schemas.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TopCandidate(BaseModel):
    name: str
    confidence: float
    confidence_percent: str


class PlantProfile(BaseModel):
    id: Optional[Any] = None
    name: str
    scientificName: str
    family: Optional[str] = "Medicinal Flora"
    nativeRegion: Optional[str] = "Asia"
    imageUrl: Optional[str] = "/images/plants/generic-leaf.jpg"
    uses: List[str] = []
    activeCompounds: List[str] = []
    partsUsed: Optional[str] = "Fresh Leaves"
    precautions: List[str] = []
    sideEffects: List[str] = []
    remedies: List[Dict[str, Any]] = []
    description: Optional[str] = None


class LeafPredictionResult(BaseModel):
    id: str
    plant: PlantProfile
    confidence: float
    confidence_percent: str
    topPredictions: List[TopCandidate]
    imageName: str
    analyzedAt: str
    model: str = "mobilenet_v2"
    status: str = "success"
    inferenceTimeMs: float = 0.0
