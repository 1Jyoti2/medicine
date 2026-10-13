"""
Main API Router Aggregator.
"""

from fastapi import APIRouter
from backend.app.api.routes import (
    leaf_router,
    pill_router,
    prescription_router,
    metadata_router,
    health_router,
)

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(leaf_router)
api_router.include_router(pill_router)
api_router.include_router(prescription_router)
api_router.include_router(metadata_router)
