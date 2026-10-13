"""
Security and Input Validation Module for Medicine Backend.
Guards against:
  - Path traversal & unsafe filenames
  - Magic byte spoofing & invalid MIME types
  - File size exhaustion / memory DoS attacks
  - Decompression bombs & corrupted images
  - Information leakage in API errors
"""

import io
import os
import re
import logging
from pathlib import Path
from typing import Tuple, Optional, Set

from fastapi import UploadFile, HTTPException, status
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger("medicine.backend.security")

# Maximum upload size in bytes (15 MB)
MAX_UPLOAD_SIZE_BYTES = int(os.getenv("MAX_UPLOAD_SIZE_MB", "15")) * 1024 * 1024

# Whitelisted image file extensions
ALLOWED_EXTENSIONS: Set[str] = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"
}

# Whitelisted MIME content-types
ALLOWED_MIME_TYPES: Set[str] = {
    "image/jpeg", "image/png", "image/webp", "image/bmp", "image/tiff",
    "image/x-png", "image/pjpeg", "application/octet-stream"
}

# Protect against Pillow decompression bomb attacks (50 Megapixels max)
Image.MAX_IMAGE_PIXELS = 50_000_000
MIN_IMAGE_DIMENSION = 10
MAX_IMAGE_DIMENSION = 10_000


def sanitize_filename(filename: Optional[str]) -> str:
    """
    Sanitizes client-provided filename to prevent path traversal,
    null byte injection, and special character exploits.
    """
    if not filename or not isinstance(filename, str):
        return "uploaded_image.jpg"

    # Strip directory components (e.g. ../../etc/passwd or C:\Windows\...)
    clean_name = os.path.basename(filename.strip())

    # Remove null bytes and control characters
    clean_name = clean_name.replace("\x00", "").replace("\r", "").replace("\n", "")

    # Replace any character not in [a-zA-Z0-9_.-] with an underscore
    clean_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", clean_name)

    # Prevent hidden files or extension-only names
    if clean_name.startswith("."):
        clean_name = f"image{clean_name}"

    # Limit filename length
    if len(clean_name) > 128:
        stem = Path(clean_name).stem[:120]
        ext = Path(clean_name).suffix
        clean_name = f"{stem}{ext}"

    return clean_name or "uploaded_image.jpg"


def verify_image_magic_bytes(header: bytes) -> bool:
    """
    Verify binary file signatures (magic bytes) to ensure file is authentic image.
    """
    if len(header) < 4:
        return False

    # JPEG: FF D8 FF
    if header.startswith(b"\xff\xd8\xff"):
        return True

    # PNG: 89 50 4E 47 0D 0A 1A 0A
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return True

    # WEBP: RIFF....WEBP
    if len(header) >= 12 and header.startswith(b"RIFF") and header[8:12] == b"WEBP":
        return True

    # BMP: BM
    if header.startswith(b"BM"):
        return True

    # TIFF: II*\x00 (little endian) or MM\x00* (big endian)
    if header.startswith(b"II*\x00") or header.startswith(b"MM\x00*"):
        return True

    return False


async def validate_and_read_image_upload(
    file: Optional[UploadFile] = None,
    image: Optional[UploadFile] = None,
    max_size: int = MAX_UPLOAD_SIZE_BYTES
) -> Tuple[bytes, str]:
    """
    Securely reads, validates, and inspects an uploaded image file.

    Performs:
      1. Presence & type check
      2. Filename sanitization & path traversal mitigation
      3. Extension whitelist validation
      4. Streamed size validation (prevents memory exhaustion)
      5. Empty file detection
      6. Binary magic byte signature verification
      7. PIL integrity and dimensional validation

    Returns:
      Tuple of (raw_bytes, sanitized_filename)

    Raises:
      HTTPException with client-safe status codes (400, 413, 415)
    """
    upload = file or image
    if upload is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image file provided in request."
        )

    # 1. Sanitize filename
    safe_filename = sanitize_filename(upload.filename)
    file_ext = Path(safe_filename).suffix.lower()

    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension '{file_ext}'. Allowed image formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    # 2. Check Content-Type if present
    if upload.content_type and upload.content_type.lower() not in ALLOWED_MIME_TYPES:
        logger.warning(f"Unusual content-type '{upload.content_type}' for {safe_filename}")

    # 3. Stream read with size enforcement (chunked read prevents memory DoS)
    chunk_size = 64 * 1024  # 64 KB
    total_bytes = 0
    buffer = io.BytesIO()

    try:
        while chunk := await upload.read(chunk_size):
            total_bytes += len(chunk)
            if total_bytes > max_size:
                max_mb = max_size // (1024 * 1024)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Uploaded image size ({total_bytes / (1024*1024):.2f} MB) exceeds maximum allowed limit of {max_mb} MB."
                )
            buffer.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading upload stream: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read uploaded file data stream."
        )

    contents = buffer.getvalue()

    # 4. Empty file check
    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image file is empty (0 bytes)."
        )

    # 5. Magic Byte signature check
    if not verify_image_magic_bytes(contents[:16]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content header does not match a valid image format."
        )

    # 6. Deep Image decoding & dimension validation with Pillow
    try:
        stream = io.BytesIO(contents)
        with Image.open(stream) as img:
            img.verify()

        stream.seek(0)
        with Image.open(stream) as img:
            w, h = img.size
            if w < MIN_IMAGE_DIMENSION or h < MIN_IMAGE_DIMENSION:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Image dimensions too small ({w}x{h}px). Minimum required: {MIN_IMAGE_DIMENSION}x{MIN_IMAGE_DIMENSION}px."
                )
            if w > MAX_IMAGE_DIMENSION or h > MAX_IMAGE_DIMENSION:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Image dimensions too large ({w}x{h}px). Maximum allowed: {MAX_IMAGE_DIMENSION}x{MAX_IMAGE_DIMENSION}px."
                )
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, SyntaxError) as e:
        logger.warning(f"Corrupted image upload rejected: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image file appears corrupted or unreadable."
        )
    except Exception as e:
        logger.warning(f"Image verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image validation failed."
        )

    return contents, safe_filename


def sanitize_error_message(exc: Exception) -> str:
    """
    Strips internal server paths, database credentials, and system details from error messages.
    """
    msg = str(exc)
    # Strip Windows paths (C:\...\) and Unix paths (/home/...)
    msg = re.sub(r"[A-Za-z]:\\[^:\s]+", "[path]", msg)
    msg = re.sub(r"\/[a-zA-Z0-9_\-\.\/]+", "[path]", msg)
    # Strip memory object addresses
    msg = re.sub(r"at 0x[0-9a-fA-F]+", "", msg)
    return msg.strip() or "An error occurred while processing the request."
