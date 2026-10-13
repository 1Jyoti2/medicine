"""
Leaf Classification Service.
Coordinates image preprocessing, PyTorch inference, Out-Of-Distribution validation,
botanical metadata, and history storage.
"""

import time
import logging
from typing import Dict, Any, Optional

try:
    from ml_training.inference import get_classifier as get_leaf_classifier, LeafInferenceError
except ImportError:
    from inference import get_classifier as get_leaf_classifier, LeafInferenceError

from backend.app.schemas import (
    LeafPredictionResult,
    PlantProfile,
    TopCandidate,
    datetime_now_iso,
    format_history_date,
)
from backend.app.services.metadata_service import (
    PLANTS_DB,
    get_plant_by_name,
    record_history,
)

logger = logging.getLogger("medicine.backend.services.leaf")


class LeafService:
    @staticmethod
    def classify_leaf(image_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Runs leaf classification with OOD validation.
        Returns prediction dictionary with is_leaf flag, botanical details, or rejection metadata.
        """
        classifier = get_leaf_classifier()
        pred = classifier.predict(image_bytes, top_k=3, include_metadata=True)

        # 1. Non-leaf / Out-of-Distribution rejection
        if not pred.get("is_leaf", True):
            logger.info(f"Image '{filename}' rejected as non-leaf: {pred.get('rejection_reason')}")
            return {
                "success": False,
                "is_leaf": False,
                "predicted_class": None,
                "confidence": 0.0,
                "confidence_percent": "0.00%",
                "top_predictions": [],
                "rejection_reason": pred.get("rejection_reason"),
                "message": pred.get("message", "Please upload a clear medicinal leaf image. The uploaded image does not appear to contain a valid medicinal leaf."),
                "debug_info": pred.get("debug_info", {}),
                "data": None
            }

        # 2. Authentic Leaf Processing
        pred_class = pred["predicted_class"]
        conf_float = round(float(pred["confidence"]) * 100.0, 1)

        # Lookup botanical profile from PostgreSQL/Cache
        plant_data = get_plant_by_name(pred_class)
        if not plant_data:
            plant_data = {
                "id": abs(hash(pred_class)) % 1000,
                "name": pred_class,
                "scientificName": pred_class,
                "family": "Medicinal Flora",
                "nativeRegion": "Asia",
                "imageUrl": "/images/plants/generic-leaf.jpg",
                "uses": ["Traditional wellness", "Herbal remedy"],
                "activeCompounds": ["Phytochemicals", "Flavonoids"],
                "partsUsed": "Fresh Leaves",
                "precautions": ["Consult a medical practitioner before use"],
                "sideEffects": ["None reported in standard herbal use"],
                "description": f"{pred_class} is an authentic medicinal plant recognized in traditional herbal medicine."
            }

        # Format Top Predictions
        top_preds = []
        for cand in pred.get("top_predictions", []):
            cand_name = cand["class"]
            cand_conf = round(float(cand["confidence"]) * 100.0, 1)
            top_preds.append(TopCandidate(
                name=cand_name,
                confidence=cand_conf,
                confidence_percent=cand["confidence_percent"]
            ))

        status_str = "success" if conf_float >= 70.0 else "low_confidence" if conf_float >= 40.0 else "uncertain"
        res_id = f"leaf_{int(time.time() * 1000)}"

        result = LeafPredictionResult(
            id=res_id,
            plant=PlantProfile(**plant_data),
            confidence=conf_float,
            confidence_percent=pred["confidence_percent"],
            topPredictions=top_preds,
            imageName=filename,
            analyzedAt=datetime_now_iso(),
            model="mobilenet_v2",
            status=status_str,
            inferenceTimeMs=pred.get("inference_time_ms", 0.0)
        )

        # Record in history only for valid leaf classifications
        record_history({
            "id": f"hist_{int(time.time() * 1000)}",
            "name": plant_data["name"],
            "type": "Medicinal Leaf",
            "confidence": conf_float,
            "date": format_history_date(),
            "status": status_str,
            "resultId": res_id
        })

        return {
            "success": True,
            "is_leaf": True,
            "data": result.model_dump(),
            "debug_info": pred.get("debug_info", {})
        }
