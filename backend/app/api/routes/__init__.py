"""
API Routes Package.
"""

from .leaf import router as leaf_router
from .pill import router as pill_router
from .prescription import router as prescription_router
from .metadata import router as metadata_router
from .health import router as health_router

__all__ = [
    "leaf_router",
    "pill_router",
    "prescription_router",
    "metadata_router",
    "health_router",
]
