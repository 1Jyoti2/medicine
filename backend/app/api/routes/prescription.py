"""
Prescription OCR & Information Extraction API Routes.
"""

import logging
from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from backend.app.core.security import validate_and_read_image_upload, sanitize_error_message
from backend.app.schemas import create_request_id
from backend.app.services import PrescriptionService

logger = logging.getLogger("medicine.backend.routes.prescription")
router = APIRouter(tags=["Prescription OCR"])


@router.post("/predict/prescription")
@router.post("/api/predict/prescription")
@router.post("/api/prescription/scan")
async def scan_prescription_endpoint(
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
):
    """
    Extracts structured handwriting text and clinical medicine entities from prescriptions.
    """
    req_id = create_request_id()
    try:
        image_bytes, filename = await validate_and_read_image_upload(file=file, image=image)
        result = PrescriptionService.scan_prescription(image_bytes, filename)
        return {
            "success": True,
            "requestId": req_id,
            "message": "Prescription scanned successfully.",
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
        logger.error(f"Prescription scan error: {e}", exc_info=True)
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "requestId": req_id,
                "message": f"Prescription OCR failed: {sanitize_error_message(e)}"
            }
        )
