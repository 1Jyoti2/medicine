"""
Root test runner for medicinal leaf classification inference.
Usage:
    python test_inference.py <path_to_image>
    python test_inference.py --all-classes
"""

import sys
from pathlib import Path

# Add ml_training directory to Python path
ml_training_dir = (Path(__file__).resolve().parent / "ml_training")
if str(ml_training_dir) not in sys.path:
    sys.path.insert(0, str(ml_training_dir))

from ml_training.test_inference import main

if __name__ == "__main__":
    main()
