"""
FastAPI Main Application Entry Point.
Production-grade, modular architecture for Medicine AI Backend.
"""

import sys
import time
import logging
from pathlib import Path
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add project root and ml_training to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "ml_training") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "ml_training"))

from backend.app.core.config import settings
from backend.app.core.security import sanitize_error_message
from backend.app.schemas import create_request_id
from backend.app.services import (
    load_databases,
    LeafService,
    PillService,
    PrescriptionService,
)
from backend.app.api.router import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("medicine.backend")

# Import ML model loaders for startup warm-up
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Preloads metadata databases and warms up ML models once at server startup.
    Eliminates first-request cold-start latency.
    """
    logger.info(f"Initializing {settings.PROJECT_NAME} [{settings.ENVIRONMENT}]...")
    startup_start = time.perf_counter()
    
    # 1. Load Botanical & Pharmaceutical Databases
    load_databases()

    # 2. Pre-warm Leaf Classifier
    try:
        leaf_cls = get_leaf_classifier()
        dummy_tensor = torch.zeros((1, 3, 224, 224), dtype=torch.float32, device=leaf_cls.device)
        with torch.inference_mode():
            leaf_cls.model(dummy_tensor)
        logger.info(f"Leaf Classifier ready & warmed up with {leaf_cls.num_classes} classes.")
    except Exception as e:
        logger.error(f"Failed to load/warmup Leaf Classifier: {e}")

    # 3. Pre-warm Prescription OCR
    try:
        ocr_pipe = get_prescription_pipeline()
        logger.info("Prescription OCR Engine ready.")
    except Exception as e:
        logger.error(f"Failed to load Prescription OCR: {e}")

    # 4. Pre-warm Pill Classifier
    try:
        pill_cls = get_pill_classifier()
        dummy_tensor = torch.zeros((1, 3, 224, 224), dtype=torch.float32, device=pill_cls.device)
        with torch.inference_mode():
            pill_cls.model(dummy_tensor)
        logger.info(f"Pill Classifier ready & warmed up with {pill_cls.num_classes} classes.")
    except Exception as e:
        logger.error(f"Failed to load/warmup Pill Classifier: {e}")

    total_startup_ms = (time.perf_counter() - startup_start) * 1000.0
    logger.info(f"All AI services preloaded and ready in {total_startup_ms:.1f}ms.")
    
    yield
    
    logger.info("Shutting down Medicine AI Services...")


# Initialize FastAPI Application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-grade AI API for Leaf Classification, Prescription OCR, and Pill Identification.",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Clean HTTP exception handler without stack trace exposure."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "requestId": create_request_id(),
            "message": sanitize_error_message(exc.detail),
            "detail": sanitize_error_message(exc.detail)
        }
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    """Global unhandled exception guard preventing internal information disclosure."""
    logger.error(f"Unhandled server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "requestId": create_request_id(),
            "message": "An internal server error occurred while processing the request."
        }
    )


# Register API Routers
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
