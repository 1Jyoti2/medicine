"""
Prescription OCR Schemas.
"""

from typing import List, Optional, Any
from pydantic import BaseModel


class PrescribedMedicine(BaseModel):
    medicineName: str
    dosage: Optional[str] = "As prescribed"
    frequency: Optional[str] = "As directed"
    duration: Optional[str] = "Course duration"
    instructions: Optional[str] = "Follow doctor instructions"
    notes: Optional[str] = "Take as directed"
    form: Optional[str] = "Tablet"
    confidence: float = 0.0
    usage: Optional[str] = None
    sideEffects: Optional[str] = None


class PrescriptionScanResult(BaseModel):
    id: str
    isHandwritten: bool = True
    prescriptionNumber: str
    patientName: str
    patientAge: Optional[str] = "Adult"
    patientSex: Optional[str] = None
    doctorName: str
    organization: str
    issuedDate: str
    diagnosis: Optional[str] = None
    extractedText: str
    medicines: List[PrescribedMedicine]
    advice: List[str] = []
    status: str = "processed"
    imageName: str
    analyzedAt: str
    overallConfidence: float = 0.0
    processingTimeMs: float = 0.0
