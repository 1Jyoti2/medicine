"""
Botanical, Medicine, and History Metadata API Routes.
"""

import logging
from fastapi import APIRouter, HTTPException, Query

from backend.app.schemas import create_request_id
from backend.app.services.metadata_service import (
    get_plant_by_name,
    get_medicine_by_name,
    get_all_history,
)

logger = logging.getLogger("medicine.backend.routes.metadata")
router = APIRouter(tags=["Metadata & History"])


@router.get("/plants/details")
@router.get("/api/plants/details")
async def get_plant_details_endpoint(name: str = Query(...)):
    """Retrieve botanical monograph details for a specific medicinal plant."""
    plant = get_plant_by_name(name)
    if plant:
        return {
            "success": True,
            "requestId": create_request_id(),
            "message": "Plant details retrieved.",
            "data": plant
        }
    raise HTTPException(status_code=404, detail=f"No plant details found for '{name}'")


@router.get("/medicines/details")
@router.get("/api/medicines/details")
async def get_medicine_details_endpoint(name: str = Query(...)):
    """Retrieve pharmaceutical medication details."""
    med = get_medicine_by_name(name)
    if med:
        return {
            "success": True,
            "requestId": create_request_id(),
            "message": "Medicine details retrieved.",
            "data": med
        }
    raise HTTPException(status_code=404, detail=f"No medicine details found for '{name}'")


@router.get("/history")
@router.get("/api/history")
async def get_history_endpoint():
    """Retrieve in-memory detection and scan session history."""
    history = get_all_history()
    return {
        "success": True,
        "requestId": create_request_id(),
        "message": "Detection history retrieved.",
        "data": history
    }
