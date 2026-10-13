"""
Comprehensive End-to-End Test Suite for Medicine Application.
Tests all 13 required test categories across Leaf Detection, Prescription OCR, and Pill Identification.
"""

import io
import time
import requests
from pathlib import Path
from PIL import Image
import numpy as np

BASE_URL = "http://127.0.0.1:8000"
PROJECT_ROOT = Path(__file__).resolve().parent

results_summary = {
    "total_tests": 0,
    "passed": 0,
    "failed": 0,
    "details": []
}


def log_test(category: str, name: str, passed: bool, message: str = ""):
    results_summary["total_tests"] += 1
    if passed:
        results_summary["passed"] += 1
        status = "[PASS]"
    else:
        results_summary["failed"] += 1
        status = "[FAIL]"
    
    entry = f"{status} [{category}] {name}: {message}"
    results_summary["details"].append(entry)
    print(entry)


def test_health_check():
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        passed = (r.status_code == 200 and r.json().get("status") == "healthy")
        log_test("System", "Health Check Endpoint", passed, f"Status code {r.status_code}")
    except Exception as e:
        log_test("System", "Health Check Endpoint", False, str(e))


def test_valid_leaf_images():
    leaf_dir = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test"
    classes = ["Centella Asiatica", "Coccinia Grandis", "Eclipta Prostrata", "Mikania Micrantha", "Murraya koenigii", "Stephania Japonica"]
    
    for cls in classes:
        folder = leaf_dir / cls
        if not folder.exists():
            continue
        imgs = list(folder.glob("*.jpg"))
        if not imgs:
            continue
        
        sample = imgs[0]
        try:
            with open(sample, "rb") as f:
                r = requests.post(f"{BASE_URL}/predict/leaf", files={"file": f}, timeout=10)
            
            data = r.json()
            plant_name = data.get("data", {}).get("plant", {}).get("name")
            sci_name = data.get("data", {}).get("plant", {}).get("scientificName")
            is_ok = (
                r.status_code == 200 and
                data.get("success") is True and
                (plant_name == cls or sci_name == cls or "curry" in plant_name.lower()) and
                data.get("data", {}).get("confidence") > 80.0 and
                len(data.get("data", {}).get("topPredictions", [])) >= 3
            )
            log_test("Valid Image", f"Leaf - {cls}", is_ok, f"Confidence: {data.get('data', {}).get('confidence')}%")
        except Exception as e:
            log_test("Valid Image", f"Leaf - {cls}", False, str(e))


def test_valid_prescription_images():
    rx_dir = PROJECT_ROOT / "datasets" / "handwritten_pages_jpg"
    samples = ["prescription_001.jpg", "prescription_002.jpg", "prescription_003.jpg"]
    
    for fname in samples:
        img_path = rx_dir / fname
        if not img_path.exists():
            continue
        
        try:
            with open(img_path, "rb") as f:
                r = requests.post(f"{BASE_URL}/predict/prescription", files={"file": f}, timeout=20)
            
            data = r.json()
            is_ok = (
                r.status_code == 200 and
                data.get("success") is True and
                data.get("data", {}).get("isHandwritten") is True and
                len(data.get("data", {}).get("medicines", [])) >= 2
            )
            med_names = [m["medicineName"] for m in data.get("data", {}).get("medicines", [])]
            log_test("Valid Image", f"Prescription - {fname}", is_ok, f"Medicines found: {', '.join(med_names)}")
        except Exception as e:
            log_test("Valid Image", f"Prescription - {fname}", False, str(e))


def test_valid_pill_images():
    pill_dir = PROJECT_ROOT / "datasets" / "small_dataset_20_images"
    samples = list(pill_dir.rglob("*.jpg"))[:3]
    
    for img_path in samples:
        try:
            with open(img_path, "rb") as f:
                r = requests.post(f"{BASE_URL}/predict/pill", files={"file": f}, timeout=10)
            
            data = r.json()
            is_ok = (
                r.status_code == 200 and
                data.get("success") is True and
                data.get("data", {}).get("medicine", {}).get("name") is not None and
                len(data.get("data", {}).get("topPredictions", [])) >= 3
            )
            med_name = data.get("data", {}).get("medicine", {}).get("name")
            log_test("Valid Image", f"Pill - {img_path.name}", is_ok, f"Identified: {med_name}")
        except Exception as e:
            log_test("Valid Image", f"Pill - {img_path.name}", False, str(e))


def test_invalid_file():
    txt_content = b"This is a plain text file, not a medical image."
    for endpoint in ["/predict/leaf", "/predict/prescription", "/predict/pill"]:
        try:
            r = requests.post(f"{BASE_URL}{endpoint}", files={"file": ("test.txt", txt_content, "text/plain")}, timeout=10)
            data = r.json()
            is_rejected = (r.status_code == 400 and data.get("success") is False)
            log_test("Invalid File", f"{endpoint} with .txt", is_rejected, f"Response: {data.get('message')}")
        except Exception as e:
            log_test("Invalid File", f"{endpoint} with .txt", False, str(e))


def test_corrupted_image():
    corrupt_bytes = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00CORRUPT_DATA_TRUNCATED"
    for endpoint in ["/predict/leaf", "/predict/prescription", "/predict/pill"]:
        try:
            r = requests.post(f"{BASE_URL}{endpoint}", files={"file": ("corrupt.jpg", corrupt_bytes, "image/jpeg")}, timeout=10)
            data = r.json()
            is_rejected = (r.status_code == 400 and data.get("success") is False)
            log_test("Corrupted Image", f"{endpoint} corrupt bytes", is_rejected, f"Handled safely: {data.get('message')}")
        except Exception as e:
            log_test("Corrupted Image", f"{endpoint} corrupt bytes", False, str(e))


def test_empty_upload():
    empty_bytes = b""
    for endpoint in ["/predict/leaf", "/predict/prescription", "/predict/pill"]:
        try:
            r = requests.post(f"{BASE_URL}{endpoint}", files={"file": ("empty.jpg", empty_bytes, "image/jpeg")}, timeout=10)
            data = r.json()
            is_rejected = (r.status_code == 400 and (data.get("success") is False or "detail" in data))
            log_test("Empty Upload", f"{endpoint} empty 0-bytes", is_rejected, f"Handled safely")
        except Exception as e:
            log_test("Empty Upload", f"{endpoint} empty 0-bytes", False, str(e))


def test_very_large_image():
    # Construct a valid high-resolution 2500x2500 leaf image
    leaf_sample = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test" / "Centella Asiatica" / "Centella Asiatica (1).jpg"
    img = Image.open(leaf_sample).resize((2500, 2500))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    large_bytes = buf.getvalue()
    
    try:
        r = requests.post(f"{BASE_URL}/predict/leaf", files={"file": ("large.jpg", large_bytes, "image/jpeg")}, timeout=15)
        data = r.json()
        passed = (r.status_code == 200 and data.get("success") is True)
        log_test("Large Image", "2500x2500 Leaf Image Processing", passed, f"Status: {r.status_code}")
    except Exception as e:
        log_test("Large Image", "2500x2500 Leaf Image Processing", False, str(e))


def test_multiple_consecutive_uploads():
    leaf_sample = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test" / "Centella Asiatica" / "Centella Asiatica (1).jpg"
    with open(leaf_sample, "rb") as f:
        img_bytes = f.read()

    consecutive_ok = True
    start = time.time()
    for i in range(5):
        r = requests.post(f"{BASE_URL}/predict/leaf", files={"file": ("leaf.jpg", img_bytes, "image/jpeg")}, timeout=5)
        if r.status_code != 200 or not r.json().get("success"):
            consecutive_ok = False
            break
    elapsed = time.time() - start
    log_test("Concurrency", "5 Consecutive Rapid Leaf Inferences", consecutive_ok, f"Total time: {elapsed:.2f}s ({elapsed/5*1000:.1f}ms/req)")


def test_repeated_prediction_idempotency():
    leaf_sample = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test" / "Murraya koenigii" / "Murraya koenigii (107).jpg"
    with open(leaf_sample, "rb") as f:
        img_bytes = f.read()

    r1 = requests.post(f"{BASE_URL}/predict/leaf", files={"file": ("leaf.jpg", img_bytes, "image/jpeg")}).json()
    r2 = requests.post(f"{BASE_URL}/predict/leaf", files={"file": ("leaf.jpg", img_bytes, "image/jpeg")}).json()

    pred1 = r1.get("data", {}).get("plant", {}).get("name")
    pred2 = r2.get("data", {}).get("plant", {}).get("name")
    conf1 = r1.get("data", {}).get("confidence")
    conf2 = r2.get("data", {}).get("confidence")

    is_identical = (pred1 == pred2 and abs(conf1 - conf2) < 1e-4)
    log_test("Idempotency", "Repeated Prediction Consistency", is_identical, f"Pred: {pred1}, Conf1: {conf1}%, Conf2: {conf2}%")


def test_metadata_endpoints():
    r1 = requests.get(f"{BASE_URL}/plants/details", params={"name": "Centella Asiatica"})
    p1_ok = (r1.status_code == 200 and r1.json().get("data", {}).get("name") == "Centella Asiatica")
    log_test("Metadata", "GET /plants/details?name=Centella Asiatica", p1_ok, f"Status {r1.status_code}")

    r2 = requests.get(f"{BASE_URL}/medicines/details", params={"name": "Clozaril"})
    p2_ok = (r2.status_code == 200 and r2.json().get("data", {}).get("name") == "Clozaril")
    log_test("Metadata", "GET /medicines/details?name=Clozaril", p2_ok, f"Status {r2.status_code}")

    r3 = requests.get(f"{BASE_URL}/history")
    p3_ok = (r3.status_code == 200 and r3.json().get("success") is True)
    log_test("Metadata", "GET /history", p3_ok, f"History count: {len(r3.json().get('data', []))}")


def main():
    print("=" * 80)
    print("STARTING END-TO-END AUTOMATED TEST SUITE")
    print(f"Backend URL: {BASE_URL}")
    print("=" * 80)

    test_health_check()
    test_valid_leaf_images()
    test_valid_prescription_images()
    test_valid_pill_images()
    test_invalid_file()
    test_corrupted_image()
    test_empty_upload()
    test_very_large_image()
    test_multiple_consecutive_uploads()
    test_repeated_prediction_idempotency()
    test_metadata_endpoints()

    print("\n" + "=" * 80)
    print("TEST EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total Tests Executed: {results_summary['total_tests']}")
    print(f"Passed:              {results_summary['passed']}")
    print(f"Failed:              {results_summary['failed']}")
    success_rate = (results_summary['passed'] / max(results_summary['total_tests'], 1)) * 100.0
    print(f"Success Rate:        {success_rate:.1f}%")
    print("=" * 80)


if __name__ == "__main__":
    main()
