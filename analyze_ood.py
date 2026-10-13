"""
OOD and Leaf vs Non-Leaf Diagnostic & Scientific Analysis Script.
Tests feature embeddings, color/vegetation metrics, logit distributions,
and discriminative power between authentic medicinal leaves and non-leaf inputs.
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

print("=== 1. COLLECTING METRICS ACROSS AUTHENTIC LEAF TEST DATASET ===")
test_dir = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed" / "test"
classes = sorted([d.name for d in test_dir.iterdir() if d.is_dir()])

leaf_metrics = []

for c in classes:
    imgs = list((test_dir / c).glob("*.jpg"))[:10]
    for img_path in imgs:
        img = Image.open(img_path).convert("RGB")
        img_np = np.array(img, dtype=np.float32)
        
        # Color & vegetation statistics
        r, g, b = img_np[:,:,0], img_np[:,:,1], img_np[:,:,2]
        total = r + g + b + 1e-6
        # Excess Green Index (ExG = 2G - R - B)
        exg = (2.0 * g - r - b) / total
        exg_mean = float(np.mean(exg))
        exg_positive_ratio = float(np.mean(exg > 0.05))
        
        # HSV Green Hue Ratio
        img_hsv = img.convert("HSV")
        hsv_np = np.array(img_hsv, dtype=np.float32)
        h = hsv_np[:,:,0] * (360.0 / 255.0)  # 0-360
        s = hsv_np[:,:,1] / 255.0
        v = hsv_np[:,:,2] / 255.0
        
        # Green hue range: 35 deg to 170 deg, saturation > 0.15, brightness > 0.15
        green_mask = (h >= 35) & (h <= 170) & (s >= 0.15) & (v >= 0.15)
        green_ratio = float(np.mean(green_mask))
        
        # Inference output
        tensor = leaf_cls.preprocessor.preprocess(img).to(device)
        with torch.inference_mode():
            feat = model.features(tensor)
            feat = torch.nn.functional.adaptive_avg_pool2d(feat, (1, 1)).flatten(1)
            logits = model.classifier(feat)
            probs = torch.softmax(logits, dim=1).cpu().squeeze().numpy()
            logits_np = logits.cpu().squeeze().numpy()
        
        # Energy Score: -log(sum(exp(logits)))
        energy = float(-np.log(np.sum(np.exp(logits_np))))
        max_logit = float(np.max(logits_np))
        entropy = float(-np.sum(probs * np.log(probs + 1e-9)))
        top_prob = float(np.max(probs))
        
        leaf_metrics.append({
            "type": "leaf",
            "class": c,
            "path": img_path.name,
            "exg_mean": exg_mean,
            "exg_positive_ratio": exg_positive_ratio,
            "green_ratio": green_ratio,
            "top_prob": top_prob,
            "max_logit": max_logit,
            "energy": energy,
            "entropy": entropy,
            "feature": feat.cpu().numpy().squeeze()
        })

print(f"Computed metrics for {len(leaf_metrics)} authentic leaf images.")

# Compute average leaf feature centroid and class centroids
all_leaf_feats = np.array([m["feature"] for m in leaf_metrics])
leaf_centroid = np.mean(all_leaf_feats, axis=0)

# ------------------------------------------------------------------------------
# 2. COLLECT METRICS FOR DIVERSE NON-LEAF IMAGES (Pills, synthetic prescriptions, random objects, skin/face tones)
# ------------------------------------------------------------------------------
print("\n=== 2. COLLECTING METRICS ACROSS NON-LEAF IMAGES ===")
non_leaf_metrics = []

# Non-leaf sources in repository: pills, prescription handwriting, synthetic images
non_leaf_imgs = []

# Prescription handwritten images
rx_dir = PROJECT_ROOT / "datasets" / "handwritten_pages_jpg"
if rx_dir.exists():
    non_leaf_imgs.extend(list(rx_dir.glob("*.jpg"))[:5])

# Pill images (white, colored, beige, blisters)
pill_dir = PROJECT_ROOT / "datasets" / "small_dataset_20_images"
if pill_dir.exists():
    non_leaf_imgs.extend(list(pill_dir.rglob("*.jpg"))[:10])

# Generate synthetic non-leaf test images: faces/skin tones, indoor room, car/metallic, textiles
def make_face_like_image():
    # Warm peach/skin tones (high red, moderate green, lower blue)
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:,:] = [225, 175, 145]  # skin tone
    # Add face features (darker eyes/hair)
    arr[60:120, 60:240] = [80, 50, 40]  # hair/eyes
    return Image.fromarray(arr)

def make_indoor_room_image():
    # Neutral grey/blue wall with wood floor
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:200, :] = [180, 190, 205]  # bluish-grey wall
    arr[200:, :] = [160, 110, 70]   # wooden floor
    return Image.fromarray(arr)

def make_car_metal_image():
    # Metallic red/silver
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:, :] = [180, 20, 30]  # red car paint
    arr[100:200, 50:250] = [200, 200, 210] # windshield
    return Image.fromarray(arr)

def make_dark_background_image():
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:, :] = [25, 25, 30]
    return Image.fromarray(arr)

synthetic_non_leaves = [
    ("face_selfie_sim", make_face_like_image()),
    ("indoor_room_sim", make_indoor_room_image()),
    ("car_metal_sim", make_car_metal_image()),
    ("dark_object_sim", make_dark_background_image()),
]

# Process real non-leaf dataset images
for p in non_leaf_imgs:
    img = Image.open(p).convert("RGB")
    synthetic_non_leaves.append((p.name, img))

for name, img in synthetic_non_leaves:
    img_np = np.array(img, dtype=np.float32)
    r, g, b = img_np[:,:,0], img_np[:,:,1], img_np[:,:,2]
    total = r + g + b + 1e-6
    exg = (2.0 * g - r - b) / total
    exg_mean = float(np.mean(exg))
    exg_positive_ratio = float(np.mean(exg > 0.05))
    
    img_hsv = img.convert("HSV")
    hsv_np = np.array(img_hsv, dtype=np.float32)
    h = hsv_np[:,:,0] * (360.0 / 255.0)
    s = hsv_np[:,:,1] / 255.0
    v = hsv_np[:,:,2] / 255.0
    green_mask = (h >= 35) & (h <= 170) & (s >= 0.15) & (v >= 0.15)
    green_ratio = float(np.mean(green_mask))
    
    tensor = leaf_cls.preprocessor.preprocess(img).to(device)
    with torch.inference_mode():
        feat = model.features(tensor)
        feat = torch.nn.functional.adaptive_avg_pool2d(feat, (1, 1)).flatten(1)
        logits = model.classifier(feat)
        probs = torch.softmax(logits, dim=1).cpu().squeeze().numpy()
        logits_np = logits.cpu().squeeze().numpy()
    
    energy = float(-np.log(np.sum(np.exp(logits_np))))
    max_logit = float(np.max(logits_np))
    entropy = float(-np.sum(probs * np.log(probs + 1e-9)))
    top_prob = float(np.max(probs))
    pred_class_idx = int(np.argmax(probs))
    pred_class_name = leaf_cls.idx_to_class.get(pred_class_idx, f"Class_{pred_class_idx}")
    
    feat_vec = feat.cpu().numpy().squeeze()
    cos_sim = float(np.dot(feat_vec, leaf_centroid) / (np.linalg.norm(feat_vec) * np.linalg.norm(leaf_centroid) + 1e-8))
    eucl_dist = float(np.linalg.norm(feat_vec - leaf_centroid))
    
    non_leaf_metrics.append({
        "type": "non_leaf",
        "name": name,
        "pred_class": pred_class_name,
        "top_prob": top_prob,
        "max_logit": max_logit,
        "energy": energy,
        "entropy": entropy,
        "green_ratio": green_ratio,
        "exg_mean": exg_mean,
        "exg_positive_ratio": exg_positive_ratio,
        "cos_sim": cos_sim,
        "dist": eucl_dist
    })

print(f"Computed metrics for {len(non_leaf_metrics)} non-leaf images.")

# ------------------------------------------------------------------------------
# 3. COMPARISON & SEPARATION ANALYSIS
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("METRIC COMPARISONS (LEAF vs NON-LEAF)")
print("=" * 80)

leaf_green = [m["green_ratio"] for m in leaf_metrics]
non_leaf_green = [m["green_ratio"] for m in non_leaf_metrics]
print(f"Green Vegetation Ratio (%):")
print(f"  Leaves:    Min={np.min(leaf_green)*100:.1f}%, Mean={np.mean(leaf_green)*100:.1f}%, Max={np.max(leaf_green)*100:.1f}%")
print(f"  Non-Leaves:Min={np.min(non_leaf_green)*100:.1f}%, Mean={np.mean(non_leaf_green)*100:.1f}%, Max={np.max(non_leaf_green)*100:.1f}%")

leaf_exg_pos = [m["exg_positive_ratio"] for m in leaf_metrics]
non_leaf_exg_pos = [m["exg_positive_ratio"] for m in non_leaf_metrics]
print(f"\nExcess Green Positive Ratio (%):")
print(f"  Leaves:    Min={np.min(leaf_exg_pos)*100:.1f}%, Mean={np.mean(leaf_exg_pos)*100:.1f}%, Max={np.max(leaf_exg_pos)*100:.1f}%")
print(f"  Non-Leaves:Min={np.min(non_leaf_exg_pos)*100:.1f}%, Mean={np.mean(non_leaf_exg_pos)*100:.1f}%, Max={np.max(non_leaf_exg_pos)*100:.1f}%")

leaf_cos = [float(np.dot(m["feature"], leaf_centroid) / (np.linalg.norm(m["feature"]) * np.linalg.norm(leaf_centroid) + 1e-8)) for m in leaf_metrics]
non_leaf_cos = [m["cos_sim"] for m in non_leaf_metrics]
print(f"\nFeature Cosine Similarity with Leaf Space Centroid:")
print(f"  Leaves:    Min={np.min(leaf_cos):.3f}, Mean={np.mean(leaf_cos):.3f}, Max={np.max(leaf_cos):.3f}")
print(f"  Non-Leaves:Min={np.min(non_leaf_cos):.3f}, Mean={np.mean(non_leaf_cos):.3f}, Max={np.max(non_leaf_cos):.3f}")

print("\nDetailed Non-Leaf Predictions (Without OOD Guard):")
for nl in non_leaf_metrics[:10]:
    print(f"  Image: {nl['name']:<25} -> Softmax Pred: {nl['pred_class']:<20} ({nl['top_prob']*100:.1f}%) | Green: {nl['green_ratio']*100:.1f}% | ExG+: {nl['exg_positive_ratio']*100:.1f}%")

print("=" * 80)
