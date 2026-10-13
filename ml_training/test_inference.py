"""
Simple test script for medicinal leaf classification inference.
Usage:
    python test_inference.py <path_to_image>
    python test_inference.py --all-classes
"""

import sys
import argparse
from pathlib import Path

# Add ml_training to sys.path if not present
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Add parent dir as well in case script is in workspace root
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

try:
    from inference import get_classifier
except ImportError:
    from ml_training.inference import get_classifier


def format_prediction_output(result: dict, image_label: str = None):
    """Format inference results cleanly for CLI output."""
    print("=" * 60)
    if image_label:
        print(f"Image: {image_label}")
    print(f"Predicted Plant: {result['predicted_class']}")
    print(f"Confidence: {result['confidence_percent']}")
    print("\nTop 3 Predictions:")
    for pred in result["top_predictions"]:
        common_str = ""
        if "common_names" in pred and pred["common_names"]:
            common_str = f" ({', '.join(pred['common_names'][:2])})"
        print(f"{pred['rank']}. {pred['class']}{common_str} - {pred['confidence_percent']}")
    
    if "plant_metadata" in result and result["plant_metadata"]:
        meta = result["plant_metadata"]
        print("\nPlant Details:")
        if "scientificName" in meta:
            print(f"  Scientific Name: {meta['scientificName']}")
        if "commonNames" in meta:
            print(f"  Common Names: {', '.join(meta['commonNames'])}")
        if "uses" in meta and meta["uses"]:
            print(f"  Key Uses: {', '.join(meta['uses'][:3])}")
    
    print(f"Inference Time: {result['inference_time_ms']:.2f} ms")
    print("=" * 60)


def test_single_image(image_path: str, model_dir: str = None):
    """Run inference test on a single image."""
    classifier = get_classifier(model_dir=model_dir)
    print("Model loaded successfully.\n")

    path = Path(image_path)
    if not path.exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    try:
        result = classifier.predict(path, top_k=3, include_metadata=True)
        format_prediction_output(result, image_label=str(path))
    except Exception as e:
        print(f"Inference Error: {e}")
        sys.exit(1)


def test_all_classes(model_dir: str = None):
    """Run inference on sample real images from all test classes."""
    classifier = get_classifier(model_dir=model_dir)
    print("Model loaded successfully.\n")
    print("Running automated validation across real test dataset samples...\n")

    # Locate test directory
    test_dir_candidates = [
        current_dir / "data" / "leaf_processed" / "test",
        current_dir / "ml_training" / "data" / "leaf_processed" / "test",
        parent_dir / "ml_training" / "data" / "leaf_processed" / "test",
        Path(r"C:\Users\Harshu\Desktop\Medicine\ml_training\data\leaf_processed\test"),
    ]

    test_dir = None
    for candidate in test_dir_candidates:
        if candidate.exists() and candidate.is_dir():
            test_dir = candidate
            break

    if not test_dir:
        print("Test dataset folder not found.")
        return

    classes = sorted([d for d in test_dir.iterdir() if d.is_dir()])
    total_tested = 0
    total_correct = 0

    for class_folder in classes:
        ground_truth = class_folder.name
        images = list(class_folder.glob("*.jpg")) + list(class_folder.glob("*.png"))
        if not images:
            continue

        sample_img = images[0]
        result = classifier.predict(sample_img, top_k=3, include_metadata=True)
        is_match = (result["predicted_class"] == ground_truth)
        total_tested += 1
        if is_match:
            total_correct += 1

        status = "MATCH" if is_match else "MISMATCH"
        print(f"[{status}] Ground Truth: {ground_truth}")
        format_prediction_output(result, image_label=sample_img.name)
        print()

    print(f"Summary: {total_correct}/{total_tested} test samples predicted correctly.")


def main():
    parser = argparse.ArgumentParser(description="Test Leaf Classification Inference")
    parser.add_argument("image_path", nargs="?", help="Path to image file")
    parser.add_argument("--model-dir", default=None, help="Path to model directory")
    parser.add_argument("--all-classes", action="store_true", help="Run test on one sample per class from test set")

    args = parser.parse_args()

    if args.all_classes or not args.image_path:
        test_all_classes(model_dir=args.model_dir)
    else:
        test_single_image(args.image_path, model_dir=args.model_dir)


if __name__ == "__main__":
    main()
