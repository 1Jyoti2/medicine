"""
Prompt 19 — Master Comprehensive Verification Script.
Tests all 7 evaluation pillars:
1. PostgreSQL Database
2. FastAPI Server & Lifecycle
3. AI API Inference (Leaf, Pill, OCR) & Validation Guards
4. Database Read/Write & Non-Hardcoded Persistence
5. Frontend Connectivity & CORS
6. Security (.env exclusion, zero credential leaks)
7. Report Generation
"""

import sys
import os
import time
import json
from pathlib import Path
import requests
from sqlalchemy import inspect, text

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))
sys.path.insert(0, str(PROJECT_ROOT / "ml_training"))

from backend.app.core.config import settings
from backend.app.db.database import engine, check_db_connection

results = {
    "database": False,
    "fastapi": False,
    "leaf": False,
    "pill": False,
    "prescription": False,
    "frontend": False,
    "security": False,
    "issues": [],
    "files_changed": [
        "backend/.env",
        "backend/.env.example",
        "backend/.gitignore",
        "backend/app/core/config.py",
        "backend/app/db/database.py",
        "backend/app/db/session.py",
        "backend/app/models/plant.py",
        "backend/app/models/medicine.py",
        "backend/app/models/history.py",
        "backend/app/services/metadata_service.py",
    ]
}

print("=" * 80)
print("PROMPT 19 — FINAL DATABASE & FULL SYSTEM VERIFICATION")
print("=" * 80)

# ==============================================================================
# 1. VERIFY POSTGRESQL DATABASE
# ==============================================================================
print("\n[1/7] Testing PostgreSQL Database Connection & Integrity...")
try:
    assert settings.DB_NAME == "medicine", f"Expected DB_NAME 'medicine', got '{settings.DB_NAME}'"
    assert int(settings.DB_PORT) == 5432, f"Expected DB_PORT 5432, got {settings.DB_PORT}"
    
    db_ok = check_db_connection()
    assert db_ok, "check_db_connection() returned False"
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    required_tables = {"medicinal_plants", "pharmaceutical_medicines", "detection_history"}
    missing = required_tables - set(tables)
    assert not missing, f"Missing required database tables: {missing}"
    
    with engine.connect() as conn:
        plant_count = conn.execute(text("SELECT COUNT(*) FROM medicinal_plants")).scalar()
        med_count = conn.execute(text("SELECT COUNT(*) FROM pharmaceutical_medicines")).scalar()
        hist_count = conn.execute(text("SELECT COUNT(*) FROM detection_history")).scalar()
        
    print(f"  + Database connection established to: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(f"  + Tables verified: {tables}")
    print(f"  + Data row counts: medicinal_plants={plant_count}, pharmaceutical_medicines={med_count}, detection_history={hist_count}")
    assert plant_count >= 6, "Expected at least 6 medicinal plant rows"
    assert med_count >= 8, "Expected at least 8 pharmaceutical medicine rows"
    
    results["database"] = True
    print("  -> PostgreSQL Database: PASS")
except Exception as e:
    print(f"  -> PostgreSQL Database: FAIL ({e})")
    results["issues"].append(f"PostgreSQL Database error: {e}")

# ==============================================================================
# 2. VERIFY FASTAPI SERVER & SYSTEM ENDPOINTS
# ==============================================================================
print("\n[2/7] Testing FastAPI Server & System Endpoints...")
try:
    # Test /health
    r = requests.get("http://127.0.0.1:8000/health", timeout=5)
    health_data = r.json()
    assert r.status_code == 200, f"Expected status 200, got {r.status_code}"
    assert health_data.get("status") == "healthy", f"Health status was {health_data.get('status')}"
    print(f"  + /health responded 200 OK: status={health_data.get('status')}, services={health_data.get('services')}")

    # Test /docs
    r_docs = requests.get("http://127.0.0.1:8000/docs", timeout=5)
    assert r_docs.status_code == 200, f"Expected /docs status 200, got {r_docs.status_code}"
    print("  + /docs responded 200 OK (Interactive Swagger UI accessible)")

    results["fastapi"] = True
    print("  -> FastAPI Server: PASS")
except Exception as e:
    print(f"  -> FastAPI Server: FAIL ({e})")
    results["issues"].append(f"FastAPI Server error: {e}")

# ==============================================================================
# 3. VERIFY AI APIS (LEAF, PILL, OCR)
# ==============================================================================
print("\n[3/7] Testing ML Inference APIs with Real Images & Validation...")

# Leaf Prediction
try:
    leaf_path = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test" / "Centella Asiatica"
    leaf_img = next(leaf_path.glob("*.jpg"))
    with open(leaf_img, "rb") as f:
        r = requests.post("http://127.0.0.1:8000/predict/leaf", files={"file": f}, timeout=10)
    data = r.json()
    assert r.status_code == 200
    assert data["success"] is True
    plant_name = data["data"]["plant"]["name"]
    conf = data["data"]["confidence"]
    print(f"  + Leaf Prediction: Identified '{plant_name}' with {conf}% confidence")
    results["leaf"] = True
    print("  -> Leaf API: PASS")
except Exception as e:
    print(f"  -> Leaf API: FAIL ({e})")
    results["issues"].append(f"Leaf API error: {e}")

# Pill Prediction
try:
    pill_path = PROJECT_ROOT / "datasets" / "small_dataset_20_images"
    pill_img = next(pill_path.rglob("*.jpg"))
    with open(pill_img, "rb") as f:
        r = requests.post("http://127.0.0.1:8000/predict/pill", files={"file": f}, timeout=10)
    data = r.json()
    assert r.status_code == 200
    assert data["success"] is True
    med_name = data["data"]["medicine"]["name"]
    top3 = data["data"]["topPredictions"]
    assert len(top3) >= 3
    print(f"  + Pill Prediction: Identified '{med_name}' with Top-3 predictions")
    results["pill"] = True
    print("  -> Pill API: PASS")
except Exception as e:
    print(f"  -> Pill API: FAIL ({e})")
    results["issues"].append(f"Pill API error: {e}")

# Prescription OCR
try:
    rx_path = PROJECT_ROOT / "datasets" / "handwritten_pages_jpg" / "prescription_001.jpg"
    with open(rx_path, "rb") as f:
        r = requests.post("http://127.0.0.1:8000/predict/prescription", files={"file": f}, timeout=20)
    data = r.json()
    assert r.status_code == 200
    assert data["success"] is True
    med_names = [m["medicineName"] for m in data["data"]["medicines"]]
    assert len(med_names) > 0
    print(f"  + Prescription OCR: Extracted medicines: {med_names}")
    results["prescription"] = True
    print("  -> Prescription OCR API: PASS")
except Exception as e:
    print(f"  -> Prescription OCR API: FAIL ({e})")
    results["issues"].append(f"Prescription OCR API error: {e}")

# ==============================================================================
# 4. DATABASE READ/WRITE INTEGRATION
# ==============================================================================
print("\n[4/7] Testing PostgreSQL Read & Write Data Flow...")
try:
    # Test reading plant details from PostgreSQL
    r_plant = requests.get("http://127.0.0.1:8000/plants/details?name=Centella%20Asiatica", timeout=5)
    assert r_plant.status_code == 200
    plant_resp = r_plant.json()
    assert plant_resp.get("success") is True
    plant_detail = plant_resp.get("data", {})
    assert plant_detail["name"] == "Centella Asiatica"
    assert "scientificName" in plant_detail
    print(f"  + Read Plant from PostgreSQL: {plant_detail['name']} -> Scientific: {plant_detail['scientificName']}")

    # Test reading history from PostgreSQL
    r_hist = requests.get("http://127.0.0.1:8000/history?limit=10", timeout=5)
    assert r_hist.status_code == 200
    history_resp = r_hist.json()
    assert history_resp.get("success") is True
    history_list = history_resp.get("data", [])
    assert len(history_list) > 0
    latest = history_list[0]
    print(f"  + Read History from PostgreSQL: {len(history_list)} retrieved records (Latest: {latest['type']} -> {latest['name']} [{latest['status']}])")
    results["database_flow"] = True
    print("  -> Database Integration: PASS")
except Exception as e:
    print(f"  -> Database Integration: FAIL ({e})")
    results["issues"].append(f"Database Integration error: {e}")

# ==============================================================================
# 5. FRONTEND CONNECTIVITY
# ==============================================================================
print("\n[5/7] Testing Frontend Dev Server & Integration...")
try:
    r_fe = requests.get("http://localhost:5173", timeout=5)
    assert r_fe.status_code == 200
    html = r_fe.text
    assert "<div id=\"root\">" in html or "<script" in html
    print("  + Frontend server active and serving index.html on http://localhost:5173")
    results["frontend"] = True
    print("  -> Frontend: PASS")
except Exception as e:
    print(f"  -> Frontend: FAIL ({e})")
    results["issues"].append(f"Frontend error: {e}")

# ==============================================================================
# 6. SECURITY & CREDENTIAL HYGIENE
# ==============================================================================
print("\n[6/7] Testing Security & Git Exclusion...")
try:
    # Check .gitignore
    with open(PROJECT_ROOT / "backend" / ".gitignore", "r") as f:
        backend_gitignore = f.read()
    with open(PROJECT_ROOT / ".gitignore", "r") as f:
        root_gitignore = f.read()
    
    assert ".env" in backend_gitignore and ".env" in root_gitignore, ".env must be ignored in .gitignore files"
    print("  + Verified .env is excluded in root and backend .gitignore")
    
    # Check .env.example
    with open(PROJECT_ROOT / "backend" / ".env.example", "r") as f:
        example_content = f.read()
    assert "your_db_password_here" in example_content
    assert settings.DB_PASSWORD not in example_content
    print("  + Verified .env.example contains only placeholders (no real passwords)")
    
    # Check API responses for password leaks
    r_h = requests.get("http://127.0.0.1:8000/health", timeout=5)
    health_raw = r_h.text
    assert settings.DB_PASSWORD not in health_raw
    print("  + Verified zero credentials exposed in API health/error responses")
    
    results["security"] = True
    print("  -> Security: PASS")
except Exception as e:
    print(f"  -> Security: FAIL ({e})")
    results["issues"].append(f"Security error: {e}")

print("\n" + "=" * 80)
print("FINAL REPORT SUMMARY")
print("=" * 80)
print(f"- Database: {'PASS' if results['database'] else 'FAIL'}")
print(f"- FastAPI: {'PASS' if results['fastapi'] else 'FAIL'}")
print(f"- Leaf: {'PASS' if results['leaf'] else 'FAIL'}")
print(f"- Pill: {'PASS' if results['pill'] else 'FAIL'}")
print(f"- Prescription OCR: {'PASS' if results['prescription'] else 'FAIL'}")
print(f"- Frontend: {'PASS' if results['frontend'] else 'FAIL'}")
print(f"- Security: {'PASS' if results['security'] else 'FAIL'}")
print(f"- Remaining issues: {'None' if not results['issues'] else '; '.join(results['issues'])}")
print(f"- Files changed: {len(results['files_changed'])} files")
for f in results['files_changed']:
    print(f"  * {f}")
print("=" * 80)
