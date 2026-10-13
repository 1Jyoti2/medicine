"""
Leaf Classification API Routes.
"""

import logging
from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from backend.app.core.security import validate_and_read_image_upload, sanitize_error_message
from backend.app.schemas import ApiResponse, create_request_id
from backend.app.services import LeafService

logger = logging.getLogger("medicine.backend.routes.leaf")
router = APIRouter(tags=["Leaf Classification"])


@router.post("/predict/leaf")
@router.post("/api/predict/leaf")
@router.post("/api/leaf/predict")
async def predict_leaf_endpoint(
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
):
    """
    Classifies medicinal plant leaf images.
    Performs real-time Out-Of-Distribution validation to reject selfies, non-leaf objects, and non-plant images.
    Returns predicted botanical profile, confidence score, top-3 candidates, and debug metadata.
    """
    req_id = create_request_id()
    try:
        image_bytes, filename = await validate_and_read_image_upload(file=file, image=image)
        result = LeafService.classify_leaf(image_bytes, filename)

        # Handle non-leaf / Out-of-Distribution rejection
        if not result.get("is_leaf", True) or not result.get("success", True):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "is_leaf": False,
                    "requestId": req_id,
                    "message": result.get("message", "Please upload a clear medicinal leaf image. The uploaded image does not appear to contain a valid medicinal leaf."),
                    "rejection_reason": result.get("rejection_reason"),
                    "debug_info": result.get("debug_info", {}),
                    "data": None
                }
            )

        return {
            "success": True,
            "is_leaf": True,
            "requestId": req_id,
            "message": "Medicinal leaf prediction completed.",
            "debug_info": result.get("debug_info", {}),
            "data": result.get("data")
        }
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "requestId": req_id,
                "message": sanitize_error_message(e.detail),
                "detail": sanitize_error_message(e.detail)
            }
        )
    except Exception as e:
        logger.error(f"Leaf prediction error: {e}", exc_info=True)
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "requestId": req_id,
                "message": f"Leaf classification failed: {sanitize_error_message(e)}"
            }
        )
