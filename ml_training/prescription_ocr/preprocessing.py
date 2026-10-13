"""
Image Preprocessing module for Prescription OCR.
Enhances handwritten and low-contrast medical prescription scans.
"""

import io
import logging
from pathlib import Path
from typing import Tuple, Union, Optional

import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger("medicine.prescription_ocr.preprocessing")


class ImageProcessingError(Exception):
    """Base exception for prescription image preprocessing errors."""
    pass


class InvalidImageError(ImageProcessingError):
    """Raised when an image is invalid, missing, or unsupported."""
    pass


class CorruptedImageError(ImageProcessingError):
    """Raised when an image is corrupted or cannot be decoded."""
    pass


class PrescriptionPreprocessor:
    """
    Production-ready preprocessor for medical prescription images.
    Performs validation, contrast enhancement (CLAHE), adaptive denoising,
    and resolution scaling to maximize OCR text recognition accuracy.
    """

    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    MIN_DIMENSION = 50  # 50px minimum width/height

    def __init__(self, target_dpi_scale: bool = True, use_clahe: bool = True):
        self.target_dpi_scale = target_dpi_scale
        self.use_clahe = use_clahe

    def validate_and_load(
        self,
        image_input: Union[str, Path, bytes, io.BytesIO, Image.Image, np.ndarray]
    ) -> np.ndarray:
        """
        Validate input source and convert to OpenCV BGR numpy array.
        """
        if isinstance(image_input, np.ndarray):
            if image_input.size == 0:
                raise InvalidImageError("Input image numpy array is empty")
            if len(image_input.shape) == 2:
                return cv2.cvtColor(image_input, cv2.COLOR_GRAY2BGR)
            return image_input

        if isinstance(image_input, Image.Image):
            try:
                rgb_img = image_input.convert("RGB")
                np_img = np.array(rgb_img)
                return cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
            except Exception as e:
                raise CorruptedImageError(f"Failed to convert PIL Image: {str(e)}")

        # Handle bytes or stream
        if isinstance(image_input, (bytes, bytearray)):
            if len(image_input) == 0:
                raise InvalidImageError("Image bytes buffer is empty")
            if len(image_input) > self.MAX_FILE_SIZE:
                raise InvalidImageError(f"Image size exceeds 50 MB limit")
            np_arr = np.frombuffer(image_input, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if img is None:
                raise CorruptedImageError("Could not decode image from provided byte stream")
            return img

        if isinstance(image_input, io.BytesIO):
            return self.validate_and_load(image_input.getvalue())

        if isinstance(image_input, (str, Path)):
            path = Path(image_input).resolve()
            if not path.exists():
                raise InvalidImageError(f"Prescription image not found at: {path}")
            if not path.is_file():
                raise InvalidImageError(f"Path is not a file: {path}")
            if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                raise InvalidImageError(f"Unsupported image extension '{path.suffix}'")
            if path.stat().st_size == 0:
                raise InvalidImageError(f"Image file is 0 bytes: {path}")

            # Verify integrity
            try:
                with Image.open(path) as pil_check:
                    pil_check.verify()
            except Exception as e:
                raise CorruptedImageError(f"Corrupted image file: {str(e)}")

            img = cv2.imread(str(path))
            if img is None:
                raise CorruptedImageError(f"Failed to read image with OpenCV: {path}")
            return img

        raise InvalidImageError(f"Unsupported image input type: {type(image_input)}")

    def enhance_image(self, bgr_img: np.ndarray) -> np.ndarray:
        """
        Enhance image contrast, remove noise, and scale up if low resolution.

        Args:
            bgr_img: OpenCV BGR image array

        Returns:
            Enhanced BGR image array ready for OCR
        """
        h, w = bgr_img.shape[:2]
        if h < self.MIN_DIMENSION or w < self.MIN_DIMENSION:
            raise InvalidImageError(f"Image dimensions ({w}x{h}) are below minimum {self.MIN_DIMENSION}px")

        # 1. Scale image to optimal OCR working resolution (800 <= width <= 1600)
        enhanced = bgr_img.copy()
        if self.target_dpi_scale:
            if w < 800:
                scale_factor = 800.0 / w
                new_w = int(w * scale_factor)
                new_h = int(h * scale_factor)
                enhanced = cv2.resize(enhanced, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            elif max(w, h) > 1600:
                scale_factor = 1600.0 / max(w, h)
                new_w = int(w * scale_factor)
                new_h = int(h * scale_factor)
                enhanced = cv2.resize(enhanced, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # 2. Fast Contrast enhancement via CLAHE in LAB color space
        if self.use_clahe:
            lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
            l_channel, a_channel, b_channel = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l_enhanced = clahe.apply(l_channel)
            lab_enhanced = cv2.merge((l_enhanced, a_channel, b_channel))
            enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

        # 3. Fast edge-preserving smoothing
        enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)

        return enhanced

    def preprocess_for_ocr(
        self,
        image_input: Union[str, Path, bytes, io.BytesIO, Image.Image, np.ndarray]
    ) -> np.ndarray:
        """
        Full pipeline: validate, load, and enhance prescription image.
        """
        bgr = self.validate_and_load(image_input)
        enhanced = self.enhance_image(bgr)
        return enhanced


def get_preprocessor() -> PrescriptionPreprocessor:
    """Factory helper to obtain a preprocessor instance."""
    return PrescriptionPreprocessor()
