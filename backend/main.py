"""
FastAPI Backend Entrypoint & Backward-Compatibility Proxy.
Exposes the modular application from backend.app.main.
"""

import sys
from pathlib import Path

# Ensure project root and subpackages are in sys.path regardless of execution CWD
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

if str(PROJECT_ROOT / "ml_training") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "ml_training"))

# Import the core modular FastAPI app
from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
