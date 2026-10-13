"""
Pill / Tablet Identification Service.
Coordinates image preprocessing, PyTorch feature extraction, gallery matching, and medicine profiles.
"""

import time
import logging
from typing import Dict, Any

try:
    from pill_identification import get_pill_classifier, PillInferenceError
except ImportError:
    from ml_training.pill_identification import get_pill_classifier, PillInferenceError

from backend.app.schemas import (
    PillPredictionResult,
    MedicineProfile,
    PillCandidate,
    datetime_now_iso,
    format_history_date,
)
from backend.app.services.metadata_service import (
    MEDICINES_DB,
    get_medicine_by_name,
    record_history,
)

logger = logging.getLogger("medicine.backend.services.pill")


class PillService:
    @staticmethod
    def identify_pill(image_bytes: bytes, filename: str) -> PillPredictionResult:
        classifier = get_pill_classifier()
        pred = classifier.predict(image_bytes, top_k=3)

        pred_class = pred.predicted_class
        conf_float = round(float(pred.confidence) * 100.0, 1)

        # Lookup or construct medicine details
        med_data = get_medicine_by_name(pred_class)
        if not med_data:
            med_data = {
                "id": f"med-{abs(hash(pred_class)) % 1000}",
                "name": pred.predicted_drug,
                "genericName": pred.generic_name,
                "category": "Prescription Medication",
                "composition": f"{pred.generic_name} {pred.strength}",
                "manufacturer": pred.manufacturer or "FDA Registered",
                "dosage": pred.strength,
                "storage": "Store in a cool, dry place away from direct sunlight.",
                "uses": ["Therapeutic clinical treatment"],
                "sideEffects": ["Consult your physician for complete side-effect profile"],
                "precautions": ["Take strictly according to prescription"],
                "description": pred.description or f"{pred.predicted_drug} ({pred.strength}) is an FDA-registered pharmaceutical medication."
            }

        # Format Top Predictions
        top_preds = []
        for cand in pred.top_predictions:
            top_preds.append(PillCandidate(
                name=cand.drug_name,
                genericName=cand.generic_name,
                strength=cand.strength,
                ndcCode=cand.ndc_code,
                confidence=round(cand.confidence * 100.0, 1),
                confidence_percent=cand.confidence_percent
            ))

        status_str = "success" if conf_float >= 10.0 else "low_confidence"
        res_id = f"tablet_{int(time.time() * 1000)}"

        result = PillPredictionResult(
            id=res_id,
            medicine=MedicineProfile(**med_data),
            confidence=conf_float,
            confidence_percent=pred.confidence_percent,
            topPredictions=top_preds,
            ndcCode=pred.ndc_code,
            imageName=filename,
            analyzedAt=datetime_now_iso(),
            model="mobilenet_v2",
            status=status_str,
            inferenceTimeMs=pred.inference_time_ms
        )

        record_history({
            "id": f"hist_{int(time.time() * 1000)}",
            "name": med_data["name"],
            "type": "Tablet",
            "confidence": conf_float,
            "date": format_history_date(),
            "status": status_str,
            "resultId": res_id
        })

        return result
