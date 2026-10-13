"""
Main FastAPI server runner.
Usage:
    python main.py
    uvicorn backend.app.main:app --reload --port 8000
"""

import sys
from pathlib import Path
import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "ml_training") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "ml_training"))

from backend.app.main import app

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
