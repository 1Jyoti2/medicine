"""
Test script for Prescription OCR and Medicine Extraction.
Usage:
    python test_ocr.py <path_to_prescription_image>
    python test_ocr.py --sample 5
    python test_ocr.py --all
"""

import sys
import os
import argparse
from pathlib import Path

# Fix Windows console encoding if needed
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add project root to sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    from prescription_ocr import get_prescription_pipeline, PrescriptionResult
except ImportError:
    from . import get_prescription_pipeline, PrescriptionResult


def print_prescription_result(result: PrescriptionResult, img_name: str = None):
    """Clean terminal display of structured prescription extraction."""
    print("=" * 70)
    print(f"PRESCRIPTION OCR ANALYSIS: {img_name or result.image_path or 'Image'}")
    print("=" * 70)

    if not result.success:
        print(f"[ERROR] Processing failed: {result.error}")
        print("=" * 70)
        return

    # 1. Header & Demographic Info
    h = result.header
    print("[CLINICAL HEADER]")
    if h.clinic_or_hospital:
        print(f"  * Clinic/Hospital: {h.clinic_or_hospital}")
    if h.doctor_name:
        qual = f" ({h.doctor_qualification})" if h.doctor_qualification else ""
        print(f"  * Prescribing Doctor: {h.doctor_name}{qual}")
    if h.patient_name:
        age_str = f", Age: {h.patient_age}" if h.patient_age else ""
        sex_str = f", Sex: {h.patient_sex}" if h.patient_sex else ""
        print(f"  * Patient: {h.patient_name}{age_str}{sex_str}")
    if h.date:
        print(f"  * Date: {h.date}")
    if h.rx_number:
        print(f"  * Rx Number: {h.rx_number}")
    if h.diagnosis:
        print(f"  * Diagnosis: {h.diagnosis}")

    # 2. Detected Medications
    print(f"\n[DETECTED MEDICATIONS] ({len(result.medicines)} found):")
    if not result.medicines:
        print("  (No specific pharmaceutical entities recognized with high confidence)")
    for i, med in enumerate(result.medicines, 1):
        print(f"  {i}. {med.name} (Confidence: {med.confidence * 100:.1f}%)")
        if med.dosage:
            print(f"     - Dosage: {med.dosage}")
        if med.form:
            print(f"     - Formulation: {med.form}")
        if med.frequency:
            print(f"     - Frequency: {med.frequency}")
        if med.duration:
            print(f"     - Duration: {med.duration}")
        if med.instructions:
            print(f"     - Instructions: {med.instructions}")
        if med.matched_generic and med.matched_generic != med.name:
            print(f"     - Generic: {med.matched_generic}")
        print(f"     - OCR Line: '{med.original_text}'")

    # 3. Advice
    if result.advice:
        print(f"\n[ADVICE / INSTRUCTIONS] ({len(result.advice)} items):")
        for adv in result.advice:
            print(f"  * {adv}")

    # 4. Summary & Metrics
    print("\n[METRICS]")
    print(f"  * Overall Confidence: {result.overall_confidence * 100:.1f}%")
    print(f"  * Processing Time: {result.processing_time_ms:.2f} ms")
    print("=" * 70)


def test_single(image_path: str):
    """Test OCR pipeline on a single image."""
    path = Path(image_path)
    if not path.exists():
        print(f"[ERROR] File not found: {image_path}")
        sys.exit(1)

    print(f"Initializing OCR pipeline for {path.name}...")
    pipeline = get_prescription_pipeline()
    result = pipeline.process_image(path)
    print_prescription_result(result, img_name=path.name)


def test_dataset(limit: int = None):
    """Test OCR pipeline across images in datasets/handwritten_pages_jpg."""
    dataset_candidates = [
        parent_dir / "datasets" / "handwritten_pages_jpg",
        parent_dir / "datasets" / "handwritten_pages_jpg (1)" / "handwritten_pages_jpg",
        Path(r"C:\Users\Harshu\Desktop\Medicine\datasets\handwritten_pages_jpg"),
    ]

    rx_dir = None
    for candidate in dataset_candidates:
        if candidate.exists() and candidate.is_dir():
            rx_dir = candidate
            break

    if not rx_dir:
        print("[ERROR] Prescription dataset folder not found.")
        sys.exit(1)

    images = sorted(list(rx_dir.glob("*.jpg")) + list(rx_dir.glob("*.png")))
    if not images:
        print(f"[ERROR] No images found in {rx_dir}")
        sys.exit(1)

    if limit:
        images = images[:limit]

    print(f"Running Prescription OCR evaluation on {len(images)} images from: {rx_dir}\n")
    pipeline = get_prescription_pipeline()

    success_count = 0
    total_meds_detected = 0

    for idx, img_path in enumerate(images, 1):
        print(f"\n[{idx}/{len(images)}] Processing {img_path.name}...")
        res = pipeline.process_image(img_path)
        if res.success:
            success_count += 1
            total_meds_detected += len(res.medicines)
        print_prescription_result(res, img_name=img_path.name)

    print("\n" + "=" * 70)
    print("PRESCRIPTION OCR EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Total Images Processed: {len(images)}")
    print(f"Successful Parses: {success_count}/{len(images)} ({success_count/len(images)*100:.1f}%)")
    print(f"Total Medications Detected: {total_meds_detected}")
    print(f"Average Medications / Prescription: {total_meds_detected/len(images):.2f}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Test Prescription OCR and Medicine Extraction")
    parser.add_argument("image_path", nargs="?", help="Path to a prescription image")
    parser.add_argument("--sample", type=int, default=None, help="Number of sample images to test")
    parser.add_argument("--all", action="store_true", help="Test all images in dataset")

    args = parser.parse_args()

    if args.image_path:
        test_single(args.image_path)
    elif args.all:
        test_dataset(limit=None)
    elif args.sample:
        test_dataset(limit=args.sample)
    else:
        # Default: test 5 sample images
        test_dataset(limit=5)


if __name__ == "__main__":
    main()
