"""
Test script for Pill Identification Inference.
Usage:
    python test_pill_inference.py <path_to_pill_image>
    python test_pill_inference.py --all
    python test_pill_inference.py --sample 5
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Configure UTF-8 encoding on Windows if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from pill_identification import get_pill_classifier, PillInferenceResult


def display_pill_result(result: PillInferenceResult, image_label: str = None):
    """Print clean formatted CLI output."""
    print("=" * 70)
    print(f"PILL IDENTIFICATION ANALYSIS: {image_label or result.image_path or 'Pill Image'}")
    print("=" * 70)

    if not result.success:
        print(f"[ERROR] Inference failed: {result.error}")
        print("=" * 70)
        return

    print(f"Predicted Pill:     {result.predicted_drug}")
    print(f"Generic Name:       {result.generic_name}")
    print(f"Strength / Form:    {result.strength} ({result.dosage_form})")
    if result.ndc_code:
        print(f"NDC Code:           {result.ndc_code}")
    if result.manufacturer:
        print(f"Manufacturer:       {result.manufacturer}")
    print(f"Confidence:         {result.confidence_percent}")
    if result.description:
        print(f"Description:        {result.description}")

    print("\nTop 3 Candidate Matches:")
    for cand in result.top_predictions:
        ndc_str = f" [NDC: {cand.ndc_code}]" if cand.ndc_code else ""
        print(f"  {cand.rank}. {cand.drug_name} ({cand.strength}) - {cand.confidence_percent}{ndc_str}")

    print(f"\nInference Time:     {result.inference_time_ms:.2f} ms")
    print("=" * 70)


def test_single_pill(image_path: str, model_dir: str = None):
    """Run inference test on a single pill image."""
    path = Path(image_path)
    if not path.exists():
        print(f"[ERROR] File not found: {image_path}")
        sys.exit(1)

    classifier = get_pill_classifier(model_dir=model_dir)
    print("Pill model loaded successfully.\n")

    result = classifier.predict(path, top_k=3)
    display_pill_result(result, image_label=path.name)


def test_dataset_pills(limit: int = None, model_dir: str = None):
    """Run validation across real images from datasets/small_dataset_20_images."""
    dataset_candidates = [
        parent_dir / "datasets" / "small_dataset_20_images",
        Path(r"C:\Users\Harshu\Desktop\Medicine\datasets\small_dataset_20_images"),
    ]

    pill_dir = None
    for cand in dataset_candidates:
        if cand.exists() and cand.is_dir():
            pill_dir = cand
            break

    if not pill_dir:
        print("[ERROR] Pill dataset directory not found.")
        sys.exit(1)

    images = sorted(list(pill_dir.rglob("*.jpg")) + list(pill_dir.rglob("*.png")))
    if not images:
        print(f"[ERROR] No pill images found in {pill_dir}")
        sys.exit(1)

    if limit:
        images = images[:limit]

    print(f"Running Pill Identification inference on {len(images)} real images...\n")
    classifier = get_pill_classifier(model_dir=model_dir)
    print("Pill model loaded successfully.\n")

    for idx, img_path in enumerate(images, 1):
        print(f"[{idx}/{len(images)}] Testing {img_path.name}...")
        res = classifier.predict(img_path, top_k=3)
        display_pill_result(res, image_label=img_path.name)
        print()


def main():
    parser = argparse.ArgumentParser(description="Test Pill Identification Inference")
    parser.add_argument("image_path", nargs="?", help="Path to pill image")
    parser.add_argument("--model-dir", default=None, help="Path to model directory")
    parser.add_argument("--sample", type=int, default=None, help="Test N sample images")
    parser.add_argument("--all", action="store_true", help="Test all images in dataset")

    args = parser.parse_args()

    if args.image_path:
        test_single_pill(args.image_path, model_dir=args.model_dir)
    elif args.all:
        test_dataset_pills(limit=None, model_dir=args.model_dir)
    elif args.sample:
        test_dataset_pills(limit=args.sample, model_dir=args.model_dir)
    else:
        test_dataset_pills(limit=4, model_dir=args.model_dir)


if __name__ == "__main__":
    main()
