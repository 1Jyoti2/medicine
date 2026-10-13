"""
Image preprocessing module for medicinal leaf classification inference.
Matches the exact preprocessing pipeline used during model training.
"""

import io
import logging
from pathlib import Path
from typing import Tuple, Union

import torch
from torchvision import transforms
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger("medicine.inference.preprocessing")


class ImageProcessingError(Exception):
    """Base exception for image processing errors."""
    pass


class InvalidImageError(ImageProcessingError):
    """Raised when an image file is invalid, unsupported, or missing."""
    pass


class CorruptedImageError(ImageProcessingError):
    """Raised when an image file is corrupted or cannot be decoded."""
    pass


class ImageDimensionError(ImageProcessingError):
    """Raised when image dimensions do not meet minimum requirements."""
    pass


class ImagePreprocessor:
    """
    Production-ready image preprocessor for leaf classification.
    Applies exact transformations used in training:
      1. Validation & decoding to RGB
      2. Direct resize to target image size (default 224x224)
      3. Conversion to PyTorch Tensor [0.0, 1.0]
      4. ImageNet normalization (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    """

    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif'}
    MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
    MIN_DIMENSION_PX = 10  # Minimum width/height in pixels

    def __init__(self, image_size: Tuple[int, int] = (224, 224)):
        """
        Initialize preprocessor with target input image size.

        Args:
            image_size: Tuple of (height, width) or (size, size)
        """
        if isinstance(image_size, (list, tuple)):
            self.image_size = (int(image_size[0]), int(image_size[1]))
        else:
            self.image_size = (int(image_size), int(image_size))

        # Standard transformation matching training pipeline
        self.transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        logger.debug(f"ImagePreprocessor initialized with target size: {self.image_size}")

    def validate_file_path(self, file_path: Union[str, Path]) -> Path:
        """
        Validate file path existence, type, extension, and size.

        Args:
            file_path: Path to the image file

        Returns:
            Path: Resolved Path object

        Raises:
            InvalidImageError: If the file is missing, not a file, invalid extension, or empty
        """
        path = Path(file_path).resolve()

        if not path.exists():
            raise InvalidImageError(f"Image file not found at: {path}")

        if not path.is_file():
            raise InvalidImageError(f"Specified path is not a file: {path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise InvalidImageError(
                f"Unsupported image extension '{path.suffix}'. "
                f"Allowed formats: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}"
            )

        file_size = path.stat().st_size
        if file_size == 0:
            raise InvalidImageError(f"Image file is empty (0 bytes): {path}")

        if file_size > self.MAX_FILE_SIZE_BYTES:
            size_mb = file_size / (1024 * 1024)
            raise InvalidImageError(
                f"Image file size ({size_mb:.2f} MB) exceeds maximum allowed limit "
                f"of {self.MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB"
            )

        return path

    def load_and_validate_pil(self, image_source: Union[str, Path, bytes, io.BytesIO, Image.Image]) -> Image.Image:
        """
        Load, verify integrity, and convert image to RGB PIL Image.

        Args:
            image_source: Path, bytes, io.BytesIO stream, or PIL Image

        Returns:
            PIL.Image.Image in RGB mode

        Raises:
            InvalidImageError / CorruptedImageError / ImageDimensionError
        """
        if isinstance(image_source, Image.Image):
            try:
                img = image_source.convert('RGB')
                w, h = img.size
                if w < self.MIN_DIMENSION_PX or h < self.MIN_DIMENSION_PX:
                    raise ImageDimensionError(
                        f"Image dimensions too small ({w}x{h}). Minimum required: {self.MIN_DIMENSION_PX}x{self.MIN_DIMENSION_PX}"
                    )
                return img
            except ImageDimensionError:
                raise
            except Exception as e:
                raise CorruptedImageError(f"Failed to process PIL Image: {str(e)}")

        # Handle bytes
        if isinstance(image_source, bytes):
            if len(image_source) == 0:
                raise InvalidImageError("Image bytes buffer is empty (0 bytes)")
            if len(image_source) > self.MAX_FILE_SIZE_BYTES:
                size_mb = len(image_source) / (1024 * 1024)
                raise InvalidImageError(f"Image bytes size ({size_mb:.2f} MB) exceeds 50 MB limit")
            stream = io.BytesIO(image_source)
        elif isinstance(image_source, io.BytesIO):
            stream = image_source
        elif isinstance(image_source, (str, Path)):
            validated_path = self.validate_file_path(image_source)
            try:
                with open(validated_path, "rb") as f:
                    stream = io.BytesIO(f.read())
            except Exception as e:
                raise InvalidImageError(f"Unable to read image file from disk: {str(e)}")
        else:
            raise InvalidImageError(f"Unsupported image input type: {type(image_source)}")

        # Single-pass decode and convert to RGB
        try:
            stream.seek(0)
            img = Image.open(stream)
            img = img.convert('RGB')
            w, h = img.size
            if w < self.MIN_DIMENSION_PX or h < self.MIN_DIMENSION_PX:
                raise ImageDimensionError(
                    f"Image dimensions too small ({w}x{h}). Minimum required: {self.MIN_DIMENSION_PX}x{self.MIN_DIMENSION_PX}"
                )
            return img
        except (UnidentifiedImageError, SyntaxError) as e:
            raise CorruptedImageError(f"Corrupted or unrecognized image format: {str(e)}")
        except ImageDimensionError:
            raise
        except (OSError, Exception) as e:
            raise CorruptedImageError(f"Failed to decode image pixels: {str(e)}")

    def preprocess(self, image_source: Union[str, Path, bytes, io.BytesIO, Image.Image]) -> torch.Tensor:
        """
        Full preprocessing pipeline: validates input, converts to RGB,
        applies Resize -> ToTensor -> Normalize, and adds batch dimension.

        Args:
            image_source: Image input (Path, string, bytes, BytesIO, or PIL Image)

        Returns:
            torch.Tensor of shape [1, 3, height, width]
        """
        pil_img = self.load_and_validate_pil(image_source)
        tensor = self.transform(pil_img)  # Shape [3, H, W]
        batch_tensor = tensor.unsqueeze(0)  # Shape [1, 3, H, W]
        return batch_tensor


def get_preprocessor(image_size: Tuple[int, int] = (224, 224)) -> ImagePreprocessor:
    """Factory helper to obtain an ImagePreprocessor instance."""
    return ImagePreprocessor(image_size=image_size)
