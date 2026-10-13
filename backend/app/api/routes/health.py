"""
System Health Check API Route.
"""

import time
import logging
from fastapi import APIRouter

try:
    from ml_training.inference import get_classifier as get_leaf_classifier
except ImportError:
    from inference import get_classifier as get_leaf_classifier

try:
    from pill_identification import get_pill_classifier
except ImportError:
    from ml_training.pill_identification import get_pill_classifier

try:
    from prescription_ocr import get_prescription_pipeline
except ImportError:
    from ml_training.prescription_ocr import get_prescription_pipeline

logger = logging.getLogger("medicine.backend.routes.health")
router = APIRouter(tags=["Health"])


@router.get("/health")
@router.get("/api/health")
async def health_check():
    """
    Health check endpoint reporting system uptime and model availability.
    Safely reports service status without exposing filesystem paths or secrets.
    """
    leaf_status = "online"
    pill_status = "online"
    ocr_status = "online"

    try:
        _ = get_leaf_classifier()
    except Exception:
        leaf_status = "offline"

    try:
        _ = get_pill_classifier()
    except Exception:
        pill_status = "offline"

    try:
        _ = get_prescription_pipeline()
    except Exception:
        ocr_status = "offline"

    return {
        "status": "healthy" if (leaf_status == "online" and pill_status == "online" and ocr_status == "online") else "degraded",
        "timestamp": time.time(),
        "services": {
            "leaf_classification": leaf_status,
            "prescription_ocr": ocr_status,
            "pill_identification": pill_status
        }
    }
