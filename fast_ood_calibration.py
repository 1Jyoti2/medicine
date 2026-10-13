"""
Fast Batched OOD Calibration and Validation Script.
Computes centroids with PyTorch batching and validates 100% of the leaf test set and non-leaf test set.
"""

import sys
import os
import json
import time
import numpy as np
from PIL import Image
from pathlib import Path
import torch

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "ml_training"))

from ml_training.inference.predictor import get_classifier

leaf_cls = get_classifier()
model = leaf_cls.model
device = leaf_cls.device

train_dir = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "train"
test_dir = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test"
classes = sorted([d.name for d in train_dir.iterdir() if d.is_dir()])

print(f"Extracting class centroids for {len(classes)} classes with batching...")

def extract_features_batch(image_paths, batch_size=32):
    features = []
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i+batch_size]
        tensors = []
        for p in batch_paths:
            img = Image.open(p).convert("RGB")
            tensors.append(leaf_cls.preprocessor.preprocess(img))
        batch_tensor = torch.cat(tensors, dim=0).to(device)
        with torch.inference_mode():
            feat = model.features(batch_tensor)
            feat = torch.nn.functional.adaptive_avg_pool2d(feat, (1, 1)).flatten(1)
            features.append(feat.cpu().numpy())
    return np.vstack(features)

centroids = {}
all_features = []
for c in classes:
    imgs = list((train_dir / c).glob("*.jpg"))[:40] # 40 per class is representative & fast
    feats = extract_features_batch(imgs)
    centroid = np.mean(feats, axis=0)
    centroid = centroid / (np.linalg.norm(centroid) + 1e-8)
    centroids[c] = centroid
    all_features.append(feats)

all_features = np.vstack(all_features)
overall_centroid = np.mean(all_features, axis=0)
overall_centroid = overall_centroid / (np.linalg.norm(overall_centroid) + 1e-8)

print("Class centroids computed.")

def test_single_image(img: Image.Image):
    img_rgb = img.convert("RGB")
    tensor = leaf_cls.preprocessor.preprocess(img_rgb).to(device)
    with torch.inference_mode():
        feat = model.features(tensor)
        feat = torch.nn.functional.adaptive_avg_pool2d(feat, (1, 1)).flatten(1)
        logits = model.classifier(feat)
        probs = torch.softmax(logits, dim=1).cpu().squeeze().numpy()
        feat_vec = feat.cpu().numpy().squeeze()
    
    feat_norm = feat_vec / (np.linalg.norm(feat_vec) + 1e-8)
    cos_sims = {c: float(np.dot(feat_norm, centroids[c])) for c in classes}
    max_cos_sim = max(cos_sims.values())
    
    # Vegetation check (ExG)
    img_np = np.array(img_rgb, dtype=np.float32)
    r, g, b = img_np[:,:,0], img_np[:,:,1], img_np[:,:,2]
    total = r + g + b + 1e-6
    exg = (2.0 * g - r - b) / total
    exg_pos_ratio = float(np.mean(exg > 0.02))
    
    # HSV Green check
    img_hsv = img_rgb.convert("HSV")
    hsv_np = np.array(img_hsv, dtype=np.float32)
    h = hsv_np[:,:,0] * (360.0 / 255.0)
    s = hsv_np[:,:,1] / 255.0
    v = hsv_np[:,:,2] / 255.0
    green_ratio = float(np.mean((h >= 30) & (h <= 175) & (s >= 0.10) & (v >= 0.10)))
    
    # Skin tone check (YCbCr)
    img_ycbcr = img_rgb.convert("YCbCr")
    ycbcr_np = np.array(img_ycbcr, dtype=np.uint8)
    cb = ycbcr_np[:,:,1]
    cr = ycbcr_np[:,:,2]
    skin_mask = (cr >= 133) & (cr <= 173) & (cb >= 77) & (cb <= 127)
    skin_ratio = float(np.mean(skin_mask))
    
    top_prob = float(np.max(probs))
    pred_idx = int(np.argmax(probs))
    pred_class = classes[pred_idx]
    
    # Decision logic:
    # 1. Feature cosine similarity must exceed threshold (0.46)
    # 2. Must not be pure skin tone without leaf features
    # 3. Softmax confidence
    is_leaf = (max_cos_sim >= 0.46) and (green_ratio > 0.005 or exg_pos_ratio > 0.01 or max_cos_sim >= 0.60) and not (skin_ratio > 0.45 and green_ratio < 0.02)
    
    return {
        "is_leaf": is_leaf,
        "pred_class": pred_class if is_leaf else None,
        "confidence": top_prob if is_leaf else 0.0,
        "raw_pred": pred_class,
        "raw_conf": top_prob,
        "max_cos_sim": max_cos_sim,
        "green_ratio": green_ratio,
        "exg_pos_ratio": exg_pos_ratio,
        "skin_ratio": skin_ratio,
    }

# 1. Test Authentic Leaves
print("\n--- Testing 60 Authentic Test Leaf Images ---")
leaf_correct = 0
leaf_total = 0
leaf_accepted = 0

for c in classes:
    for p in (test_dir / c).glob("*.jpg"):
        img = Image.open(p)
        res = test_single_image(img)
        leaf_total += 1
        if res["is_leaf"]:
            leaf_accepted += 1
            if res["pred_class"] == c:
                leaf_correct += 1

print(f"Authentic Leaves Evaluated: {leaf_total}")
print(f"Accepted as Leaf: {leaf_accepted} / {leaf_total} ({leaf_accepted/leaf_total*100:.1f}%)")
print(f"Correct Classification: {leaf_correct} / {leaf_total} ({leaf_correct/leaf_total*100:.1f}%)")

# 2. Test Non-Leaf Images
print("\n--- Testing Non-Leaf Images (Selfies, Faces, Prescriptions, Pills, Objects) ---")
non_leaves = []
# Selfies / Faces
for tone in [[240, 190, 160], [210, 150, 110], [160, 100, 70], [100, 60, 40]]:
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:,:] = tone
    arr[40:100, 60:240] = [50, 30, 20]
    arr[160:200, 100:200] = [180, 80, 80]
    non_leaves.append(("Selfie/Person (Skin Tone " + str(tone) + ")", Image.fromarray(arr)))

# Objects, Prescriptions, Pills
for p in (PROJECT_ROOT / "datasets" / "handwritten_pages_jpg").glob("*.jpg"):
    non_leaves.append(("Prescription " + p.name, Image.open(p)))
for p in list((PROJECT_ROOT / "datasets" / "small_dataset_20_images").rglob("*.jpg"))[:10]:
    non_leaves.append(("Pill " + p.name, Image.open(p)))

nl_rejected = 0
for name, img in non_leaves:
    res = test_single_image(img)
    if not res["is_leaf"]:
        nl_rejected += 1
        print(f"  [REJECTED non-leaf] {name:<35} -> MaxSim: {res['max_cos_sim']:.3f}, Green: {res['green_ratio']*100:.1f}%, Skin: {res['skin_ratio']*100:.1f}%")
    else:
        print(f"  [FALSE ACCEPT]      {name:<35} -> RawPred: {res['raw_pred']} ({res['raw_conf']*100:.1f}%), MaxSim: {res['max_cos_sim']:.3f}")

print(f"\nNon-Leaves Evaluated: {len(non_leaves)}")
print(f"Correctly Rejected: {nl_rejected} / {len(non_leaves)} ({nl_rejected/len(non_leaves)*100:.1f}%)")

# Save the calibrated centroids to model directory for inference use
centroid_export = {
    "classes": classes,
    "class_centroids": {c: centroids[c].tolist() for c in classes},
    "overall_centroid": overall_centroid.tolist(),
    "similarity_threshold": 0.46,
}
with open(PROJECT_ROOT / "ml_training" / "models" / "training_20260919_135002" / "leaf_ood_centroids.json", "w") as f:
    json.dump(centroid_export, f, indent=2)

print("\nSaved leaf_ood_centroids.json successfully.")
