"""
Prescription OCR Package.
Production-ready medical handwriting text extraction and medicine entity detection.
"""

import time
import logging
from typing import Union, Any, Optional, Dict, List
from pathlib import Path

from .schemas import (
    MedicineItem,
    PrescriptionHeader,
    PrescriptionResult,
)
from .preprocessing import (
    PrescriptionPreprocessor,
    get_preprocessor,
    ImageProcessingError,
    InvalidImageError,
    CorruptedImageError,
)
from .ocr_engine import (
    PrescriptionOCREngine,
    get_ocr_engine,
    OCREngineError,
)
from .medicine_extractor import (
    MedicineExtractor,
    get_medicine_extractor,
)

logger = logging.getLogger("medicine.prescription_ocr")


class PrescriptionOCRPipeline:
    """
    End-to-end Prescription OCR and Entity Extraction pipeline.
    Connects Image Preprocessing -> EasyOCR Engine -> Medicine Extractor.
    """

    def __init__(self, gpu: bool = False):
        self.preprocessor = get_preprocessor()
        self.ocr_engine = get_ocr_engine(gpu=gpu)
        self.extractor = get_medicine_extractor()

    def process_image(
        self,
        image_input: Union[str, Path, bytes, Any],
        enhance: bool = True,
    ) -> PrescriptionResult:
        """
        Run full OCR pipeline on prescription image.

        Args:
            image_input: File path, raw bytes, PIL Image, or numpy array.
            enhance: Apply CLAHE contrast enhancement & scaling.

        Returns:
            PrescriptionResult dataclass with structured prescription data.
        """
        start_time = time.perf_counter()
        img_path_str = str(image_input) if isinstance(image_input, (str, Path)) else None

        try:
            # 1. OCR Extraction (includes preprocessing internally)
            ocr_output = self.ocr_engine.run_ocr(image_input, enhance=enhance)

            # 2. Extract structured entities
            result = self.extractor.process(ocr_output, image_path=img_path_str)

            total_elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            result.processing_time_ms = round(total_elapsed_ms, 2)
            return result

        except Exception as e:
            total_elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error(f"Prescription OCR pipeline error: {e}", exc_info=True)
            return PrescriptionResult(
                success=False,
                image_path=img_path_str,
                error=str(e),
                processing_time_ms=round(total_elapsed_ms, 2),
            )


# Singleton Pipeline Instance
_pipeline_instance: Optional[PrescriptionOCRPipeline] = None


def get_prescription_pipeline(gpu: bool = False) -> PrescriptionOCRPipeline:
    """Get singleton pipeline instance."""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = PrescriptionOCRPipeline(gpu=gpu)
    return _pipeline_instance


def process_prescription(image_input: Union[str, Path, bytes, Any], gpu: bool = False) -> PrescriptionResult:
    """Convenience function to run prescription OCR pipeline."""
    pipeline = get_prescription_pipeline(gpu=gpu)
    return pipeline.process_image(image_input)


__all__ = [
    "PrescriptionOCRPipeline",
    "get_prescription_pipeline",
    "process_prescription",
    "PrescriptionOCREngine",
    "get_ocr_engine",
    "PrescriptionPreprocessor",
    "get_preprocessor",
    "MedicineExtractor",
    "get_medicine_extractor",
    "MedicineItem",
    "PrescriptionHeader",
    "PrescriptionResult",
    "ImageProcessingError",
    "InvalidImageError",
    "CorruptedImageError",
    "OCREngineError",
]

__version__ = "1.0.0"
