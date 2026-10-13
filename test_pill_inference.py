"""
Root test runner for Pill Identification Inference.
Usage:
    python test_pill_inference.py <path_to_pill_image>
    python test_pill_inference.py --sample 4
    python test_pill_inference.py --all
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from pill_identification.test_pill_inference import main

if __name__ == "__main__":
    main()
