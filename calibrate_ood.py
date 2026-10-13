"""
OOD Calibration Script.
Computes centroids and tests boundary separation across 100% of the test set and diverse non-leaf images.
"""

import sys
import os
import json
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

print(f"Building Class Centroids from Training Set across {len(classes)} classes...")
train_features_by_class = {c: [] for c in classes}
all_train_features = []

for c in classes:
    imgs = list((train_dir / c).glob("*.jpg"))
    for p in imgs:
        img = Image.open(p).convert("RGB")
        tensor = leaf_cls.preprocessor.preprocess(img).to(device)
        with torch.inference_mode():
            feat = model.features(tensor)
            feat = torch.nn.functional.adaptive_avg_pool2d(feat, (1, 1)).flatten(1)
            feat_np = feat.cpu().numpy().squeeze()
        train_features_by_class[c].append(feat_np)
        all_train_features.append(feat_np)

centroids = {}
for c in classes:
    centroids[c] = np.mean(train_features_by_class[c], axis=0)
    # Normalize centroid
    centroids[c] = centroids[c] / (np.linalg.norm(centroids[c]) + 1e-8)

overall_centroid = np.mean(all_train_features, axis=0)
overall_centroid = overall_centroid / (np.linalg.norm(overall_centroid) + 1e-8)

print("Centroids computed.")

def evaluate_sample(img: Image.Image):
    img_rgb = img.convert("RGB")
    tensor = leaf_cls.preprocessor.preprocess(img_rgb).to(device)
    with torch.inference_mode():
        feat = model.features(tensor)
        feat = torch.nn.functional.adaptive_avg_pool2d(feat, (1, 1)).flatten(1)
        logits = model.classifier(feat)
        probs = torch.softmax(logits, dim=1).cpu().squeeze().numpy()
        feat_vec = feat.cpu().numpy().squeeze()
    
    feat_norm = feat_vec / (np.linalg.norm(feat_vec) + 1e-8)
    
    # Cosine similarities to each class centroid
    cos_sims = {c: float(np.dot(feat_norm, centroids[c])) for c in classes}
    max_cos_sim = max(cos_sims.values())
    overall_cos_sim = float(np.dot(feat_norm, overall_centroid))
    
    # Botanical color features
    img_np = np.array(img_rgb, dtype=np.float32)
    r, g, b = img_np[:,:,0], img_np[:,:,1], img_np[:,:,2]
    total = r + g + b + 1e-6
    exg = (2.0 * g - r - b) / total
    exg_pos_ratio = float(np.mean(exg > 0.03))
    
    img_hsv = img_rgb.convert("HSV")
    hsv_np = np.array(img_hsv, dtype=np.float32)
    h = hsv_np[:,:,0] * (360.0 / 255.0)
    s = hsv_np[:,:,1] / 255.0
    v = hsv_np[:,:,2] / 255.0
    green_ratio = float(np.mean((h >= 30) & (h <= 175) & (s >= 0.12) & (v >= 0.12)))
    
    # Skin tone detection (in YCbCr space: Cr ~ [133, 173], Cb ~ [77, 127])
    img_ycbcr = img_rgb.convert("YCbCr")
    ycbcr_np = np.array(img_ycbcr, dtype=np.uint8)
    cb = ycbcr_np[:,:,1]
    cr = ycbcr_np[:,:,2]
    skin_mask = (cr >= 133) & (cr <= 173) & (cb >= 77) & (cb <= 127)
    skin_ratio = float(np.mean(skin_mask))
    
    top_prob = float(np.max(probs))
    pred_idx = int(np.argmax(probs))
    pred_class = classes[pred_idx]
    
    return {
        "pred_class": pred_class,
        "top_prob": top_prob,
        "max_cos_sim": max_cos_sim,
        "overall_cos_sim": overall_cos_sim,
        "green_ratio": green_ratio,
        "exg_pos_ratio": exg_pos_ratio,
        "skin_ratio": skin_ratio,
        "cos_sims": cos_sims
    }

# Test all test leaves
test_leaf_results = []
for c in classes:
    for p in (test_dir / c).glob("*.jpg"):
        img = Image.open(p)
        res = evaluate_sample(img)
        res["true_class"] = c
        res["path"] = str(p)
        test_leaf_results.append(res)

print(f"Evaluated {len(test_leaf_results)} TEST leaves.")
leaf_max_sims = [r["max_cos_sim"] for r in test_leaf_results]
leaf_overall_sims = [r["overall_cos_sim"] for r in test_leaf_results]
print(f"Test Leaf Max Cosine Sim: Min={min(leaf_max_sims):.4f}, Mean={np.mean(leaf_max_sims):.4f}, Max={max(leaf_max_sims):.4f}")
print(f"Test Leaf Overall Cosine Sim: Min={min(leaf_overall_sims):.4f}, Mean={np.mean(leaf_overall_sims):.4f}")

# Test diverse Non-Leaf images
non_leaf_samples = []
# 1. Synthetic Faces / Selfies (various skin tones)
for tone in [[240, 190, 160], [210, 150, 110], [160, 100, 70], [100, 60, 40]]:
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:,:] = tone
    arr[40:100, 60:240] = [50, 30, 20]  # hair/eyes
    arr[160:200, 100:200] = [180, 80, 80] # lips
    non_leaf_samples.append(("Synthetic Face Tone " + str(tone), Image.fromarray(arr)))

# 2. Indoor rooms, cars, dark scenes
for p in (PROJECT_ROOT / "datasets" / "handwritten_pages_jpg").glob("*.jpg"):
    non_leaf_samples.append(("Prescription " + p.name, Image.open(p)))
for p in list((PROJECT_ROOT / "datasets" / "small_dataset_20_images").rglob("*.jpg"))[:15]:
    non_leaf_samples.append(("Pill " + p.name, Image.open(p)))

non_leaf_results = []
for name, img in non_leaf_samples:
    res = evaluate_sample(img)
    res["name"] = name
    non_leaf_results.append(res)

print(f"\nEvaluated {len(non_leaf_results)} NON-LEAF images.")
nl_max_sims = [r["max_cos_sim"] for r in non_leaf_results]
print(f"Non-Leaf Max Cosine Sim: Min={min(nl_max_sims):.4f}, Mean={np.mean(nl_max_sims):.4f}, Max={max(nl_max_sims):.4f}")

print("\n--- Summary of Decision Boundary ---")
print(f"Leaf Max Cosine Sim Min: {min(leaf_max_sims):.4f}")
print(f"Non-Leaf Max Cosine Sim Max: {max(nl_max_sims):.4f}")
print(f"Separation Margin: {min(leaf_max_sims) - max(nl_max_sims):.4f}")

# Save centroids for production inference
centroid_data = {
    "classes": classes,
    "class_centroids": {c: centroids[c].tolist() for c in classes},
    "overall_centroid": overall_centroid.tolist(),
    "min_leaf_similarity": float(min(leaf_max_sims)),
    "recommended_similarity_threshold": 0.48,
    "recommended_min_green_or_exg": 0.015,
}
with open(PROJECT_ROOT / "ml_training" / "models" / "training_20260919_135002" / "leaf_ood_centroids.json", "w") as f:
    json.dump(centroid_data, f, indent=2)

print("Saved leaf_ood_centroids.json successfully.")
