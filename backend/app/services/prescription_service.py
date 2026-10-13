"""
Prescription OCR Service.
Coordinates image preprocessing, EasyOCR execution, clinical regex parsing, and structured scan responses.
"""

import time
import logging
from typing import Dict, Any

try:
    from prescription_ocr import get_prescription_pipeline, PrescriptionResult
except ImportError:
    from ml_training.prescription_ocr import get_prescription_pipeline, PrescriptionResult

from backend.app.schemas import (
    PrescriptionScanResult,
    PrescribedMedicine,
    datetime_now_iso,
    format_history_date,
)
from backend.app.services.metadata_service import record_history

logger = logging.getLogger("medicine.backend.services.prescription")


class PrescriptionService:
    @staticmethod
    def scan_prescription(image_bytes: bytes, filename: str) -> PrescriptionScanResult:
        pipeline = get_prescription_pipeline()
        result: PrescriptionResult = pipeline.process_image(image_bytes)

        if not result.success:
            raise RuntimeError(result.error or "OCR processing was unsuccessful")

        h = result.header
        medicines_list = []
        for med in result.medicines:
            medicines_list.append(PrescribedMedicine(
                medicineName=med.name,
                dosage=med.dosage or "As prescribed",
                frequency=med.frequency or "As directed",
                duration=med.duration or "Course duration",
                instructions=med.instructions or med.dosage or "Follow doctor instructions",
                notes=med.instructions or "Take as directed",
                form=med.form or "Tablet",
                confidence=round(med.confidence * 100.0, 1),
                usage=med.usage or "As prescribed for diagnosed condition",
                sideEffects=med.side_effects or "Mild nausea, drowsiness, or dizziness (consult physician if persistent)"
            ))

        rx_number = h.rx_number or f"RX-{int(time.time()) % 10000:04d}"
        patient_name = h.patient_name or "Patient"
        doctor_name = h.doctor_name or "Consulting Physician"
        organization = h.clinic_or_hospital or "Medical Health Center"
        issued_date = h.date or time.strftime("%Y-%m-%d")
        res_id = f"rx_{int(time.time() * 1000)}"

        scan_result = PrescriptionScanResult(
            id=res_id,
            isHandwritten=True,
            prescriptionNumber=rx_number,
            patientName=patient_name,
            patientAge=h.patient_age or "Adult",
            patientSex=h.patient_sex,
            doctorName=doctor_name,
            organization=organization,
            issuedDate=issued_date,
            diagnosis=h.diagnosis,
            extractedText=result.raw_text or "No text recognized",
            medicines=medicines_list,
            advice=result.advice,
            status="processed",
            imageName=filename,
            analyzedAt=datetime_now_iso(),
            overallConfidence=round(result.overall_confidence * 100.0, 1),
            processingTimeMs=result.processing_time_ms
        )

        record_history({
            "id": f"hist_{int(time.time() * 1000)}",
            "name": patient_name,
            "type": "Prescription",
            "confidence": round(result.overall_confidence * 100.0, 1),
            "date": format_history_date(),
            "status": "processed",
            "resultId": res_id
        })

        return scan_result
