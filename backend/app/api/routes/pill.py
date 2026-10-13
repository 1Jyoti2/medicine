"""
Pill & Tablet Identification API Routes.
"""

import logging
from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from backend.app.core.security import validate_and_read_image_upload, sanitize_error_message
from backend.app.schemas import create_request_id
from backend.app.services import PillService

logger = logging.getLogger("medicine.backend.routes.pill")
router = APIRouter(tags=["Pill Identification"])


@router.post("/predict/pill")
@router.post("/api/predict/pill")
@router.post("/api/tablet/predict")
async def predict_pill_endpoint(
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
):
    """
    Identifies pharmaceutical pills and tablets from uploaded photographs.
    """
    req_id = create_request_id()
    try:
        image_bytes, filename = await validate_and_read_image_upload(file=file, image=image)
        result = PillService.identify_pill(image_bytes, filename)
        return {
            "success": True,
            "requestId": req_id,
            "message": "Pharmaceutical tablet prediction completed.",
            "data": result.model_dump()
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
        logger.error(f"Pill identification error: {e}", exc_info=True)
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "requestId": req_id,
                "message": f"Pill identification failed: {sanitize_error_message(e)}"
            }
        )
