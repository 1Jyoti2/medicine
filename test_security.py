"""
Security & Input Validation Verification Suite for Medicine Application.
Validates all 15 security areas from Prompt 11.
"""

import io
import os
import time
import requests
from PIL import Image
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
PROJECT_ROOT = Path(__file__).resolve().parent

test_results = []


def record(test_name: str, passed: bool, detail: str = ""):
    status = "[PASS]" if passed else "[FAIL]"
    msg = f"{status} {test_name}: {detail}"
    test_results.append((test_name, passed, detail))
    print(msg)


def test_path_traversal_filename():
    """Test path traversal attempts in filename parameters."""
    leaf_samples = list((PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test").rglob("*.jpg"))
    if not leaf_samples:
        leaf_samples = list((PROJECT_ROOT / "ml_training" / "data" / "leaf_processed").rglob("*.jpg"))
    with open(leaf_samples[0], "rb") as f:
        img_bytes = f.read()

    malicious_filenames = [
        ("../../../../../../windows/system32/cmd.exe.jpg", True),
        ("..\\..\\..\\..\\secret.jpg", True),
        ("nested/dir/evil.jpg", True),
        ("/etc/passwd.jpg", True),
        ("....//....//shell.php.jpg", True),
        ("../../etc/passwd", False)  # Disallowed extension without .jpg
    ]

    for fname, should_accept in malicious_filenames:
        try:
            r = requests.post(
                f"{BASE_URL}/predict/leaf",
                files={"file": (fname, img_bytes, "image/jpeg")},
                timeout=10
            )
            data = r.json()
            if should_accept:
                sanitized_name = data.get("data", {}).get("imageName", "")
                is_safe = (
                    r.status_code == 200 and
                    ".." not in sanitized_name and
                    "/" not in sanitized_name and
                    "\\" not in sanitized_name and
                    len(sanitized_name) > 0
                )
                record(f"Path Traversal Guard ({fname[:25]}...)", is_safe, f"Sanitized to: '{sanitized_name}'")
            else:
                is_safe = (r.status_code == 400 and data.get("success") is False)
                record(f"Disallowed File Extension ({fname[:25]}...)", is_safe, f"Rejected cleanly: {data.get('message')}")
        except Exception as e:
            record(f"Path Traversal Guard ({fname[:25]}...)", False, str(e))


def test_null_byte_injection():
    """Test null byte injection in filenames."""
    leaf_sample = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test" / "Centella Asiatica" / "Centella Asiatica (1).jpg"
    with open(leaf_sample, "rb") as f:
        img_bytes = f.read()

    try:
        r = requests.post(
            f"{BASE_URL}/predict/leaf",
            files={"file": ("test\x00malicious.exe.jpg", img_bytes, "image/jpeg")},
            timeout=10
        )
        data = r.json()
        sanitized_name = data.get("data", {}).get("imageName", "")
        is_safe = (r.status_code == 200 and "\x00" not in sanitized_name)
        record("Null Byte Injection Guard", is_safe, f"Sanitized to: '{sanitized_name}'")
    except Exception as e:
        record("Null Byte Injection Guard", False, str(e))


def test_disallowed_file_extensions():
    """Test non-image extensions (.exe, .sh, .py, .php, .html)."""
    payload = b"print('Hello dangerous payload')"
    extensions = [".exe", ".sh", ".py", ".php", ".html", ".js", ".bin"]

    for ext in extensions:
        try:
            r = requests.post(
                f"{BASE_URL}/predict/leaf",
                files={"file": (f"exploit{ext}", payload, "application/octet-stream")},
                timeout=10
            )
            data = r.json()
            is_blocked = (r.status_code == 400 and data.get("success") is False)
            record(f"Block Extension '{ext}'", is_blocked, f"Status: {r.status_code}, Msg: {data.get('message')}")
        except Exception as e:
            record(f"Block Extension '{ext}'", False, str(e))


def test_magic_byte_spoofing():
    """Test fake image extension with non-image binary payload."""
    fake_payload = b"PK\x03\x04This is a zip file disguised as jpg"
    try:
        r = requests.post(
            f"{BASE_URL}/predict/leaf",
            files={"file": ("disguised.jpg", fake_payload, "image/jpeg")},
            timeout=10
        )
        data = r.json()
        is_blocked = (r.status_code == 400 and data.get("success") is False)
        record("Magic Byte Verification (ZIP disguised as JPG)", is_blocked, f"Msg: {data.get('message')}")
    except Exception as e:
        record("Magic Byte Verification (ZIP disguised as JPG)", False, str(e))


def test_empty_file_rejection():
    """Test zero-byte uploads across all 3 endpoints."""
    for endpoint in ["/predict/leaf", "/predict/prescription", "/predict/pill"]:
        try:
            r = requests.post(
                f"{BASE_URL}{endpoint}",
                files={"file": ("empty.jpg", b"", "image/jpeg")},
                timeout=10
            )
            data = r.json()
            is_blocked = (r.status_code == 400 and data.get("success") is False)
            record(f"Empty File Rejection ({endpoint})", is_blocked, f"Msg: {data.get('message')}")
        except Exception as e:
            record(f"Empty File Rejection ({endpoint})", False, str(e))


def test_corrupted_image_rejection():
    """Test truncated/corrupted JPEG."""
    corrupt_bytes = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00CORRUPT_TAIL"
    for endpoint in ["/predict/leaf", "/predict/prescription", "/predict/pill"]:
        try:
            r = requests.post(
                f"{BASE_URL}{endpoint}",
                files={"file": ("corrupt.jpg", corrupt_bytes, "image/jpeg")},
                timeout=10
            )
            data = r.json()
            is_blocked = (r.status_code == 400 and data.get("success") is False)
            record(f"Corrupted Image Guard ({endpoint})", is_blocked, f"Msg: {data.get('message')}")
        except Exception as e:
            record(f"Corrupted Image Guard ({endpoint})", False, str(e))


def test_no_stack_trace_leakage():
    """Verify error messages never expose local paths or tracebacks."""
    try:
        r = requests.post(
            f"{BASE_URL}/predict/leaf",
            files={"file": ("invalid.txt", b"plain text", "text/plain")},
            timeout=10
        )
        data = r.json()
        raw_resp = r.text
        has_path = "C:\\" in raw_resp or "/Users/" in raw_resp or "/home/" in raw_resp
        has_traceback = "Traceback (most recent call last)" in raw_resp
        is_clean = (not has_path and not has_traceback)
        record("Information Leakage Guard (No paths/stack traces in API response)", is_clean, f"Response: {data.get('message')}")
    except Exception as e:
        record("Information Leakage Guard", False, str(e))


def test_cors_headers():
    """Verify CORS response headers."""
    try:
        r = requests.options(f"{BASE_URL}/predict/leaf", headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST"
        }, timeout=5)
        allow_origin = r.headers.get("access-control-allow-origin")
        is_ok = allow_origin is not None
        record("CORS Configuration", is_ok, f"Allow-Origin header: {allow_origin}")
    except Exception as e:
        record("CORS Configuration", False, str(e))


def test_functional_predictions_after_hardening():
    """Verify all 3 predictions remain 100% functional with real images."""
    # 1. Leaf
    leaf_samples = list((PROJECT_ROOT / "ml_training" / "data" / "leaf_processed").rglob("*.jpg"))
    if leaf_samples:
        leaf_sample = leaf_samples[0]
        with open(leaf_sample, "rb") as f:
            r_leaf = requests.post(f"{BASE_URL}/predict/leaf", files={"file": f}, timeout=10)
        leaf_ok = (r_leaf.status_code == 200 and r_leaf.json().get("success") is True and r_leaf.json().get("data", {}).get("plant", {}).get("name") is not None)
        record(f"Real Leaf Prediction ({leaf_sample.parent.name})", leaf_ok, f"Plant: {r_leaf.json().get('data', {}).get('plant', {}).get('name')}, Confidence: {r_leaf.json().get('data', {}).get('confidence')}%")

    # 2. Prescription
    rx_samples = list((PROJECT_ROOT / "datasets" / "handwritten_pages_jpg").glob("*.jpg"))
    if rx_samples:
        rx_sample = rx_samples[0]
        with open(rx_sample, "rb") as f:
            r_rx = requests.post(f"{BASE_URL}/predict/prescription", files={"file": f}, timeout=15)
        rx_ok = (r_rx.status_code == 200 and r_rx.json().get("success") is True and len(r_rx.json().get("data", {}).get("medicines", [])) >= 2)
        record(f"Real Prescription OCR ({rx_sample.name})", rx_ok, f"Medicines found: {len(r_rx.json().get('data', {}).get('medicines', []))}")

    # 3. Pill
    pill_samples = list((PROJECT_ROOT / "datasets" / "small_dataset_20_images").rglob("*.jpg"))
    if pill_samples:
        pill_sample = pill_samples[0]
        with open(pill_sample, "rb") as f:
            r_pill = requests.post(f"{BASE_URL}/predict/pill", files={"file": f}, timeout=10)
        pill_ok = (r_pill.status_code == 200 and r_pill.json().get("success") is True and r_pill.json().get("data", {}).get("medicine", {}).get("name") is not None)
        record(f"Real Pill Identification ({pill_sample.parent.name})", pill_ok, f"Drug: {r_pill.json().get('data', {}).get('medicine', {}).get('name')}")


def main():
    print("=" * 80)
    print("STARTING SECURITY & INPUT VALIDATION TEST SUITE")
    print(f"Target URL: {BASE_URL}")
    print("=" * 80)

    test_path_traversal_filename()
    test_null_byte_injection()
    test_disallowed_file_extensions()
    test_magic_byte_spoofing()
    test_empty_file_rejection()
    test_corrupted_image_rejection()
    test_no_stack_trace_leakage()
    test_cors_headers()
    test_functional_predictions_after_hardening()

    print("\n" + "=" * 80)
    print("SECURITY SUITE SUMMARY")
    print("=" * 80)
    total = len(test_results)
    passed = sum(1 for _, p, _ in test_results if p)
    failed = total - passed
    print(f"Total Security Tests: {total}")
    print(f"Passed:               {passed}")
    print(f"Failed:               {failed}")
    print(f"Success Rate:         {(passed/total)*100.0:.1f}%")
    print("=" * 80)


if __name__ == "__main__":
    main()
