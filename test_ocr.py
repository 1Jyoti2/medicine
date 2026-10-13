"""
Root test runner for Prescription OCR and Medicine Extraction.
Usage:
    python test_ocr.py <path_to_prescription_image>
    python test_ocr.py --sample 5
    python test_ocr.py --all
"""

import sys
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from prescription_ocr.test_ocr import main

if __name__ == "__main__":
    main()
