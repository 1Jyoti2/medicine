"""
Data schemas for Prescription OCR and Medicine Extraction.
Defines strongly-typed representations of extracted prescription entities.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class MedicineItem:
    """Represents a single detected medication and its dosage instructions."""
    name: str                                # Standardized/detected drug name
    original_text: str                       # Raw line/text segment from OCR
    dosage: Optional[str] = None             # e.g., "500 mg", "10 mg", "400 mg"
    form: Optional[str] = None               # e.g., "Tablet", "Capsule", "Syrup", "Lotion", "Inhalation"
    frequency: Optional[str] = None          # e.g., "Thrice daily", "Twice daily", "Once daily", "At night"
    duration: Optional[str] = None           # e.g., "5 days", "3 days", "30 days"
    instructions: Optional[str] = None       # e.g., "After food", "Before breakfast", "Apply locally"
    confidence: float = 0.0                  # Confidence score (0.0 to 1.0)
    matched_generic: Optional[str] = None    # Standard generic pharmacological name

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PrescriptionHeader:
    """Demographic, administrative, and clinical header information."""
    clinic_or_hospital: Optional[str] = None
    doctor_name: Optional[str] = None
    doctor_qualification: Optional[str] = None
    doctor_reg_no: Optional[str] = None
    patient_name: Optional[str] = None
    patient_age: Optional[str] = None
    patient_sex: Optional[str] = None
    date: Optional[str] = None
    rx_number: Optional[str] = None
    diagnosis: Optional[str] = None
    contact: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PrescriptionResult:
    """Full structured output of the Prescription OCR pipeline."""
    success: bool
    image_path: Optional[str] = None
    header: PrescriptionHeader = field(default_factory=PrescriptionHeader)
    medicines: List[MedicineItem] = field(default_factory=list)
    advice: List[str] = field(default_factory=list)
    raw_text: str = ""
    raw_lines: List[str] = field(default_factory=list)
    overall_confidence: float = 0.0
    processing_time_ms: float = 0.0
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        return res
