"""
HTTP API Test for Leaf Classification & Non-Leaf Rejection.
"""

import io
import json
import numpy as np
from PIL import Image
from pathlib import Path
import requests

PROJECT_ROOT = Path(__file__).resolve().parent
BASE_URL = "http://127.0.0.1:8000"

print("=" * 80)
print("TESTING HTTP API: POST /predict/leaf")
print("=" * 80)

# 1. Test Real Leaf Image Upload
leaf_img_path = next((PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test" / "Centella Asiatica").glob("*.jpg"))
with open(leaf_img_path, "rb") as f:
    resp = requests.post(f"{BASE_URL}/predict/leaf", files={"file": ("centella_sample.jpg", f, "image/jpeg")})

print("\n--- 1. REAL LEAF UPLOAD ---")
print("HTTP Status Code:", resp.status_code)
leaf_json = resp.json()
print("Success:", leaf_json.get("success"))
print("Is Leaf:", leaf_json.get("is_leaf"))
print("Message:", leaf_json.get("message"))
if leaf_json.get("data"):
    print("Plant Name:", leaf_json["data"]["plant"]["name"])
    print("Confidence:", leaf_json["data"]["confidence"])
    print("Uses:", leaf_json["data"]["plant"]["uses"][:2])
assert resp.status_code == 200
assert leaf_json["success"] is True
assert leaf_json["is_leaf"] is True
assert leaf_json["data"]["plant"]["name"] == "Centella Asiatica"
print("-> REAL LEAF HTTP TEST: PASS")

# 2. Test Real Selfie / Face Image Upload
arr_selfie = np.zeros((300, 300, 3), dtype=np.uint8)
arr_selfie[:, :] = [225, 175, 145]
arr_selfie[50:100, 60:240] = [50, 30, 20]
arr_selfie[160:200, 100:200] = [180, 80, 80]
img_bytes = io.BytesIO()
Image.fromarray(arr_selfie).save(img_bytes, format="JPEG")
img_bytes.seek(0)

resp_selfie = requests.post(f"{BASE_URL}/predict/leaf", files={"file": ("user_selfie.jpg", img_bytes, "image/jpeg")})

print("\n--- 2. SELFIE / FACE UPLOAD ---")
print("HTTP Status Code:", resp_selfie.status_code)
selfie_json = resp_selfie.json()
print("Success:", selfie_json.get("success"))
print("Is Leaf:", selfie_json.get("is_leaf"))
print("Message:", selfie_json.get("message"))
print("Data:", selfie_json.get("data"))
print("Rejection Reason:", selfie_json.get("rejection_reason"))
assert resp_selfie.status_code == 400
assert selfie_json["success"] is False
assert selfie_json["is_leaf"] is False
assert selfie_json["data"] is None
assert "Please upload a clear medicinal leaf image" in selfie_json["message"]
print("-> SELFIE / NON-LEAF REJECTION HTTP TEST: PASS")

# 3. Test Object / Non-Leaf Image Upload (Pill/Room)
arr_room = np.zeros((300, 300, 3), dtype=np.uint8)
arr_room[:200, :] = [180, 190, 205]
arr_room[200:, :] = [160, 110, 70]
img_room_bytes = io.BytesIO()
Image.fromarray(arr_room).save(img_room_bytes, format="JPEG")
img_room_bytes.seek(0)

resp_room = requests.post(f"{BASE_URL}/predict/leaf", files={"file": ("room_furniture.jpg", img_room_bytes, "image/jpeg")})

print("\n--- 3. OBJECT / ROOM UPLOAD ---")
print("HTTP Status Code:", resp_room.status_code)
room_json = resp_room.json()
print("Success:", room_json.get("success"))
print("Is Leaf:", room_json.get("is_leaf"))
print("Message:", room_json.get("message"))
assert resp_room.status_code == 400
assert room_json["success"] is False
assert room_json["is_leaf"] is False
assert room_json["data"] is None
print("-> ROOM / OBJECT REJECTION HTTP TEST: PASS")

print("\n" + "=" * 80)
print("ALL HTTP LEAF API TESTS PASSED SUCCESSFULLY")
print("=" * 80)
