"""
Image Preprocessing module for Pill Identification.
Validates, decodes, resizes, and normalizes pill images for CNN inference.
"""

import io
import logging
from pathlib import Path
from typing import Tuple, Union, Any

import torch
from torchvision import transforms
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger("medicine.pill_identification.preprocessing")


class PillImageError(Exception):
    """Base exception for pill image preprocessing."""
    pass


class InvalidPillImageError(PillImageError):
    """Raised when pill image is missing, empty, or unsupported."""
    pass


class CorruptedPillImageError(PillImageError):
    """Raised when pill image file cannot be opened or is corrupted."""
    pass


class PillPreprocessor:
    """
    Standard image preprocessor for pill identification CNN models.
    Applies Resize(224, 224) -> ToTensor() -> ImageNet Normalization.
    """

    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    MIN_DIMENSION = 20

    def __init__(self, image_size: Tuple[int, int] = (224, 224)):
        self.image_size = image_size
        self.transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def load_and_validate(self, image_input: Union[str, Path, bytes, io.BytesIO, Image.Image]) -> Image.Image:
        """
        Validate and load input image as RGB PIL Image.
        """
        if isinstance(image_input, Image.Image):
            return image_input.convert("RGB")

        if isinstance(image_input, (bytes, bytearray)):
            if len(image_input) == 0:
                raise InvalidPillImageError("Image byte buffer is empty")
            if len(image_input) > self.MAX_FILE_SIZE:
                raise InvalidPillImageError("Image byte size exceeds 50 MB limit")
            stream = io.BytesIO(image_input)
        elif isinstance(image_input, io.BytesIO):
            stream = image_input
        elif isinstance(image_input, (str, Path)):
            path = Path(image_input).resolve()
            if not path.exists():
                raise InvalidPillImageError(f"Pill image file not found: {path}")
            if not path.is_file():
                raise InvalidPillImageError(f"Path is not a regular file: {path}")
            if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                raise InvalidPillImageError(f"Unsupported image extension '{path.suffix}'")
            if path.stat().st_size == 0:
                raise InvalidPillImageError(f"Pill image file is empty: {path}")

            try:
                with open(path, "rb") as f:
                    stream = io.BytesIO(f.read())
            except Exception as e:
                raise InvalidPillImageError(f"Cannot read image file from disk: {e}")
        else:
            raise InvalidPillImageError(f"Unsupported image type: {type(image_input)}")

        # Single-pass decode and convert to RGB
        try:
            stream.seek(0)
            img = Image.open(stream).convert("RGB")
            w, h = img.size
            if w < self.MIN_DIMENSION or h < self.MIN_DIMENSION:
                raise InvalidPillImageError(f"Image too small ({w}x{h}). Minimum {self.MIN_DIMENSION}px")
            return img
        except (UnidentifiedImageError, SyntaxError) as e:
            raise CorruptedPillImageError(f"Corrupted pill image: {e}")
        except PillImageError:
            raise
        except (OSError, Exception) as e:
            raise CorruptedPillImageError(f"Failed to decode image pixels: {e}")

    def preprocess(self, image_input: Union[str, Path, bytes, io.BytesIO, Image.Image]) -> torch.Tensor:
        """
        Validate, load, transform, and add batch dimension.
        Returns: [1, 3, 224, 224] Tensor.
        """
        pil_img = self.load_and_validate(image_input)
        tensor = self.transform(pil_img)
        return tensor.unsqueeze(0)


def get_preprocessor(image_size: Tuple[int, int] = (224, 224)) -> PillPreprocessor:
    """Factory helper to obtain a PillPreprocessor."""
    return PillPreprocessor(image_size=image_size)
