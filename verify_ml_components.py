"""
Comprehensive standalone verification script for all 3 ML components.
"""

import sys
import os
import json
import torch
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "ml_training"))
sys.path.insert(0, str(PROJECT_ROOT / "pill_training"))
sys.path.insert(0, str(PROJECT_ROOT / "pill_identification"))
sys.path.insert(0, str(PROJECT_ROOT / "prescription_ocr"))

print("=" * 80)
print("VERIFYING ALL 3 ML COMPONENTS: LEAF, PILL, AND PRESCRIPTION OCR")
print("=" * 80)

# ------------------------------------------------------------------------------
# 1. LEAF CLASSIFICATION
# ------------------------------------------------------------------------------
print("\n--- 1. LEAF CLASSIFICATION ---")
leaf_dataset_path = PROJECT_ROOT / "ml_training" / "data" / "leaf_processed"
leaf_train_script = PROJECT_ROOT / "ml_training" / "train.py"
print(f"Dataset Path: {leaf_dataset_path} (Exists: {leaf_dataset_path.exists()})")
print(f"Training Script: {leaf_train_script} (Exists: {leaf_train_script.exists()})")

from ml_training.inference.predictor import get_classifier
leaf_cls = get_classifier()
print(f"Model Path: {leaf_cls.model_path}")
print(f"Model File Size: {Path(leaf_cls.model_path).stat().st_size / (1024*1024):.2f} MB")
print(f"Model Architecture: {leaf_cls.config.get('model_type', leaf_cls.config.get('architecture', 'mobilenet_v2'))}")
print(f"Total Classes: {len(leaf_cls.classes)}")
print(f"Classes: {leaf_cls.classes}")

sample_leaf = next((leaf_dataset_path / "test" / "Centella Asiatica").glob("*.jpg"))
leaf_pred = leaf_cls.predict(sample_leaf)
print(f"Test Image: {sample_leaf}")
print(f"Predicted Class: {leaf_pred['predicted_class']}")
print(f"Confidence: {leaf_pred['confidence']*100:.2f}%")
top3_leaf = [(p['class'], f"{p['confidence']*100:.2f}%") for p in leaf_pred['top_predictions']]
print(f"Top-3 Predictions: {top3_leaf}")

# ------------------------------------------------------------------------------
# 2. PILL IDENTIFICATION
# ------------------------------------------------------------------------------
print("\n--- 2. PILL IDENTIFICATION ---")
pill_dataset_path = PROJECT_ROOT / "datasets" / "small_dataset_20_images"
pill_train_script = PROJECT_ROOT / "pill_training" / "train_pill_classifier.py"
if not pill_train_script.exists():
    pill_train_script = PROJECT_ROOT / "pill_training" / "train.py"
print(f"Dataset Path: {pill_dataset_path} (Exists: {pill_dataset_path.exists()})")
print(f"Training Script: {pill_train_script} (Exists: {pill_train_script.exists()})")

from pill_identification.predictor import get_pill_classifier
pill_cls = get_pill_classifier()
print(f"Model Path: {pill_cls.model_path}")
print(f"Model File Size: {Path(pill_cls.model_path).stat().st_size / (1024*1024):.2f} MB")
print(f"Model Architecture: {pill_cls.config.get('architecture', 'mobilenet_v2')}")
print(f"Total Classes: {len(pill_cls.classes)}")
print(f"Classes: {pill_cls.classes}")

sample_pill = next(pill_dataset_path.rglob("*.jpg"))
pill_pred = pill_cls.predict(sample_pill)
print(f"Test Image: {sample_pill}")
print(f"Predicted Drug: {pill_pred.predicted_drug} ({pill_pred.predicted_class})")
print(f"Generic Name: {pill_pred.generic_name}")
print(f"NDC Code: {pill_pred.ndc_code}")
print(f"Confidence: {pill_pred.confidence*100:.2f}%")
top3_pill = [(c.drug_name, c.confidence_percent) for c in pill_pred.top_predictions]
print(f"Top-3 Predictions: {top3_pill}")

# ------------------------------------------------------------------------------
# 3. PRESCRIPTION OCR
# ------------------------------------------------------------------------------
print("\n--- 3. PRESCRIPTION OCR ---")
rx_dataset_path = PROJECT_ROOT / "datasets" / "handwritten_pages_jpg"
rx_engine_script = PROJECT_ROOT / "prescription_ocr" / "ocr_engine.py"
rx_extractor_script = PROJECT_ROOT / "prescription_ocr" / "medicine_extractor.py"
print(f"Dataset Path: {rx_dataset_path} (Exists: {rx_dataset_path.exists()})")
print(f"OCR Engine Script: {rx_engine_script} (Exists: {rx_engine_script.exists()})")
print(f"Medicine Extractor Script: {rx_extractor_script} (Exists: {rx_extractor_script.exists()})")

craft_model = Path(os.path.expanduser("~")) / ".EasyOCR" / "model" / "craft_mlt_25k.pth"
recog_model = Path(os.path.expanduser("~")) / ".EasyOCR" / "model" / "english_g2.pth"
print(f"CRAFT Detector Model: {craft_model} ({craft_model.stat().st_size / (1024*1024):.2f} MB)")
print(f"Recognition Model: {recog_model} ({recog_model.stat().st_size / (1024*1024):.2f} MB)")

from prescription_ocr import get_prescription_pipeline
ocr_pipe = get_prescription_pipeline()

sample_rx = rx_dataset_path / "prescription_001.jpg"
rx_res = ocr_pipe.process_image(sample_rx)
print(f"Test Image: {sample_rx}")
print(f"Raw Text Extracted:\n{rx_res.raw_text.strip()}")
print(f"Matched Medicines: {[(m.name, m.dosage, m.frequency, m.duration) for m in rx_res.medicines]}")
print(f"Patient Name: {rx_res.header.patient_name}")
print(f"Doctor Name: {rx_res.header.doctor_name}")
print(f"Diagnosis: {rx_res.header.diagnosis}")
print("=" * 80)
