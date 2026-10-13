"""
Verification script for modular FastAPI backend structure.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_structure():
    print("Testing Backend Health & Documentation...")
    r_health = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"GET /health -> Status: {r_health.status_code}, Body: {r_health.json()}")
    assert r_health.status_code == 200
    assert r_health.json().get("status") == "healthy"

    r_docs = requests.get(f"{BASE_URL}/docs", timeout=5)
    print(f"GET /docs -> Status: {r_docs.status_code}")
    assert r_docs.status_code == 200

    r_openapi = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
    print(f"GET /openapi.json -> Status: {r_openapi.status_code}")
    assert r_openapi.status_code == 200
    paths = list(r_openapi.json().get("paths", {}).keys())
    print(f"Registered Endpoints ({len(paths)}): {paths}")

    print("\nALL BACKEND STRUCTURE TESTS PASSED!")

if __name__ == "__main__":
    test_structure()
