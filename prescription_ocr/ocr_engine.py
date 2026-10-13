"""
OCR Engine module using EasyOCR for prescription text extraction.
Implements thread-safe singleton initialization and line grouping.
"""

import logging
import threading
import time
from typing import List, Dict, Any, Tuple, Optional, Union
from pathlib import Path
import numpy as np

import easyocr

from .preprocessing import (
    PrescriptionPreprocessor,
    get_preprocessor,
    InvalidImageError,
    CorruptedImageError,
)

logger = logging.getLogger("medicine.prescription_ocr.ocr_engine")


class OCREngineError(Exception):
    """Base exception for OCR engine execution."""
    pass


class PrescriptionOCREngine:
    """
    Production-grade OCR Engine for prescriptions.
    Wraps EasyOCR with image enhancement, line clustering, and confidence scoring.
    """

    def __init__(self, languages: Optional[List[str]] = None, gpu: bool = False):
        self.languages = languages or ["en"]
        self.gpu = gpu
        self.preprocessor = get_preprocessor()

        logger.info(f"Initializing EasyOCR Reader (languages={self.languages}, gpu={self.gpu})...")
        self.reader = easyocr.Reader(self.languages, gpu=self.gpu, verbose=False)
        logger.info("EasyOCR Reader successfully initialized.")

    def run_ocr(
        self,
        image_input: Union[str, Path, bytes, np.ndarray, Any],
        enhance: bool = True,
        min_confidence: float = 0.05,
    ) -> Dict[str, Any]:
        """
        Run OCR on an image and extract structured text lines.

        Args:
            image_input: Path, bytes, PIL Image, or numpy array
            enhance: Whether to apply contrast enhancement & scaling
            min_confidence: Minimum score to include detected box

        Returns:
            dict with 'raw_results', 'lines', 'full_text', 'average_confidence'
        """
        start_time = time.perf_counter()

        try:
            if enhance:
                img_array = self.preprocessor.preprocess_for_ocr(image_input)
            else:
                img_array = self.preprocessor.validate_and_load(image_input)

            # EasyOCR expects RGB or numpy array
            results = self.reader.readtext(
                img_array,
                detail=1,
                paragraph=False,
                contrast_ths=0.1,
                adjust_contrast=0.5,
            )

            # Format raw detections: [(bbox, text, conf), ...]
            detections = []
            for bbox, text, conf in results:
                text_clean = text.strip()
                if text_clean and conf >= min_confidence:
                    detections.append({
                        "bbox": bbox,
                        "text": text_clean,
                        "confidence": float(conf),
                        "center_y": (bbox[0][1] + bbox[2][1]) / 2.0,
                        "center_x": (bbox[0][0] + bbox[1][0]) / 2.0,
                        "height": abs(bbox[2][1] - bbox[0][1]),
                    })

            # Cluster bounding boxes into lines based on Y-overlap
            lines = self._group_detections_into_lines(detections)
            full_text = "\n".join(lines)

            avg_conf = (
                float(np.mean([d["confidence"] for d in detections]))
                if detections else 0.0
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            return {
                "detections": detections,
                "lines": lines,
                "full_text": full_text,
                "average_confidence": round(avg_conf, 4),
                "elapsed_ms": round(elapsed_ms, 2),
            }

        except (InvalidImageError, CorruptedImageError):
            raise
        except Exception as e:
            logger.error(f"OCR execution failed: {e}", exc_info=True)
            raise OCREngineError(f"EasyOCR text extraction failed: {str(e)}")

    def _group_detections_into_lines(self, detections: List[Dict[str, Any]]) -> List[str]:
        """
        Cluster detections by vertical coordinate into sequential lines.
        """
        if not detections:
            return []

        # Sort detections primarily by top-to-bottom center_y
        sorted_dets = sorted(detections, key=lambda d: d["center_y"])

        line_groups: List[List[Dict[str, Any]]] = []
        for det in sorted_dets:
            placed = False
            for group in line_groups:
                # Check if center_y is within line vertical threshold (approx half box height)
                avg_y = np.mean([d["center_y"] for d in group])
                avg_h = np.mean([d["height"] for d in group])
                threshold = max(15.0, avg_h * 0.7)

                if abs(det["center_y"] - avg_y) <= threshold:
                    group.append(det)
                    placed = True
                    break

            if not placed:
                line_groups.append([det])

        # Sort boxes within each line horizontally (left to right)
        merged_lines = []
        for group in line_groups:
            group.sort(key=lambda d: d["center_x"])
            line_text = " ".join(d["text"] for d in group)
            if line_text:
                merged_lines.append(line_text)

        return merged_lines


# Thread-safe global singleton
_ocr_lock = threading.Lock()
_global_ocr_engine: Optional[PrescriptionOCREngine] = None


def get_ocr_engine(gpu: bool = False) -> PrescriptionOCREngine:
    """
    Get or initialize the singleton OCR engine instance.
    Loads models into memory once.
    """
    global _global_ocr_engine
    if _global_ocr_engine is None:
        with _ocr_lock:
            if _global_ocr_engine is None:
                _global_ocr_engine = PrescriptionOCREngine(gpu=gpu)
    return _global_ocr_engine
