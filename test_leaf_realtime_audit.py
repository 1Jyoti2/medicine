"""
Prompt — Real-Time Leaf Prediction Audit and Fix Test Suite.
Tests:
- Group A: Valid leaves across all 6 classes
- Group B: Non-leaf inputs (human face/selfie, room, car, prescription, pill, dark scene)
- Group C: Difficult inputs (dark, bright, blurry, cropped)
"""

import sys
import os
import io
import time
import json
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path
import requests

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "ml_training"))

from ml_training.inference.predictor import get_classifier

leaf_cls = get_classifier()
test_dir = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test"
classes = sorted([d.name for d in test_dir.iterdir() if d.is_dir()])

print("=" * 80)
print("REAL-TIME LEAF PREDICTION AUDIT & VERIFICATION TEST SUITE")
print("=" * 80)

# ==============================================================================
# TEST GROUP A — VALID LEAVES
# ==============================================================================
print("\n" + "=" * 80)
print("TEST GROUP A — VALID MEDICINAL LEAVES (6 Classes)")
print("=" * 80)

group_a_results = []
for c in classes:
    imgs = list((test_dir / c).glob("*.jpg"))[:3]
    for p in imgs:
        pred = leaf_cls.predict(p)
        is_ok = (pred["is_leaf"] is True) and (pred["predicted_class"] == c)
        conf = pred["confidence"] * 100.0
        status = "[PASS]" if is_ok else "[FAIL]"
        print(f"  {status} True Class: {c:<22} -> Predicted: {str(pred['predicted_class']):<22} | Conf: {conf:5.1f}% | MaxSim: {pred['debug_info']['max_cosine_similarity']:.3f}")
        group_a_results.append({
            "true_class": c,
            "pred_class": pred["predicted_class"],
            "conf": conf,
            "is_leaf": pred["is_leaf"],
            "passed": is_ok
        })

group_a_pass = sum(1 for r in group_a_results if r["passed"])
print(f"\nGroup A Summary: {group_a_pass}/{len(group_a_results)} passed ({group_a_pass/len(group_a_results)*100:.1f}%)")

# ==============================================================================
# TEST GROUP B — NON-LEAF INPUTS
# ==============================================================================
print("\n" + "=" * 80)
print("TEST GROUP B — NON-LEAF INPUTS (Faces, Selfies, Objects, Rooms, Pills, Rx)")
print("=" * 80)

non_leaf_tests = []

# 1. Human Selfie / Face (different skin tones and lighting)
for label, tone in [
    ("Human Selfie (Fair Skin Tone)", [240, 195, 165]),
    ("Human Selfie (Medium Skin Tone)", [205, 145, 105]),
    ("Human Selfie (Deep Skin Tone)", [140, 85, 55]),
    ("Human Selfie (Dark Skin Tone)", [85, 50, 35]),
]:
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:, :] = tone
    arr[40:90, 60:240] = [40, 25, 15]   # Hair / eyes
    arr[160:190, 100:200] = [170, 75, 75] # Mouth
    non_leaf_tests.append((label, Image.fromarray(arr)))

# 2. Indoor Room Background
arr_room = np.zeros((300, 300, 3), dtype=np.uint8)
arr_room[:200, :] = [185, 195, 210] # Blue-grey wall
arr_room[200:, :] = [160, 115, 75]  # Wood floor
non_leaf_tests.append(("Indoor Room / Furniture", Image.fromarray(arr_room)))

# 3. Metallic / Vehicle Scene
arr_car = np.zeros((300, 300, 3), dtype=np.uint8)
arr_car[:, :] = [180, 25, 35] # Red metallic
arr_car[80:180, 50:250] = [210, 215, 225] # Glass
non_leaf_tests.append(("Vehicle / Metallic Object", Image.fromarray(arr_car)))

# 4. Handwritten Prescriptions
for p in list((PROJECT_ROOT / "datasets" / "handwritten_pages_jpg").glob("*.jpg"))[:3]:
    non_leaf_tests.append((f"Prescription ({p.name})", Image.open(p)))

# 5. Pharmaceutical Pills
for p in list((PROJECT_ROOT / "datasets" / "small_dataset_20_images").rglob("*.jpg"))[:3]:
    non_leaf_tests.append((f"Pill ({p.name})", Image.open(p)))

group_b_results = []
for label, img in non_leaf_tests:
    pred = leaf_cls.predict(img)
    is_rejected = (pred["is_leaf"] is False)
    status = "[PASS - REJECTED]" if is_rejected else "[FAIL - FALSE ACCEPT]"
    reason = pred.get("rejection_reason", "Accepted as leaf")
    max_sim = pred["debug_info"]["max_cosine_similarity"]
    print(f"  {status} Input: {label:<35} -> Rejected: {is_rejected} | MaxSim: {max_sim:.3f} | Reason: {reason}")
    group_b_results.append({
        "label": label,
        "is_rejected": is_rejected,
        "max_sim": max_sim,
        "reason": reason
    })

group_b_pass = sum(1 for r in group_b_results if r["is_rejected"])
print(f"\nGroup B Summary: {group_b_pass}/{len(group_b_results)} correctly rejected ({group_b_pass/len(group_b_results)*100:.1f}%)")

# ==============================================================================
# TEST GROUP C — DIFFICULT LEAF INPUTS
# ==============================================================================
print("\n" + "=" * 80)
print("TEST GROUP C — DIFFICULT LEAF INPUTS (Blurry, Dark, Bright, Partial, Rotated)")
print("=" * 80)

sample_leaf_path = next((test_dir / "Centella Asiatica").glob("*.jpg"))
base_img = Image.open(sample_leaf_path).convert("RGB")

difficult_tests = [
    ("Blurry Leaf (Gaussian Blur r=4)", base_img.filter(ImageFilter.GaussianBlur(radius=4))),
    ("Very Dark Leaf (Brightness 0.4x)", ImageEnhance.Brightness(base_img).enhance(0.4)),
    ("Very Bright Leaf (Brightness 1.6x)", ImageEnhance.Brightness(base_img).enhance(1.6)),
    ("Low Contrast Leaf (Contrast 0.5x)", ImageEnhance.Contrast(base_img).enhance(0.5)),
    ("Partial Crop (Center 60% Crop)", base_img.crop((40, 40, base_img.width-40, base_img.height-40))),
    ("Rotated Leaf (45 deg Rotation)", base_img.rotate(45, expand=False)),
]

group_c_results = []
for label, img in difficult_tests:
    pred = leaf_cls.predict(img)
    is_accepted = (pred["is_leaf"] is True)
    conf = pred["confidence"] * 100.0
    status = "[PASS]" if is_accepted else "[WARNING]"
    print(f"  {status} Condition: {label:<38} -> Is Leaf: {is_accepted} | Pred: {str(pred['predicted_class']):<20} | Conf: {conf:5.1f}%")
    group_c_results.append({
        "label": label,
        "is_accepted": is_accepted,
        "pred": pred["predicted_class"],
        "conf": conf
    })

group_c_pass = sum(1 for r in group_c_results if r["is_accepted"])
print(f"\nGroup C Summary: {group_c_pass}/{len(group_c_results)} recognized ({group_c_pass/len(group_c_results)*100:.1f}%)")

print("\n" + "=" * 80)
print("AUDIT & VERIFICATION COMPLETE")
print("=" * 80)
