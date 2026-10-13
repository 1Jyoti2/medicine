"""
Quick test of prescription OCR on a single image
"""
import sys
from pathlib import Path

# Test without full processing first
print("Testing prescription OCR setup...")

# Check if dataset exists
dataset_path = Path("c:/Users/Harshu/Desktop/Medicine/datasets/handwritten_pages_jpg (1)/handwritten_pages_jpg")
if not dataset_path.exists():
    print(f"❌ Dataset not found at: {dataset_path}")
    sys.exit(1)

images = list(dataset_path.glob("*.jpg"))
print(f"✓ Found {len(images)} prescription images")

if len(images) == 0:
    print("❌ No images found in dataset")
    sys.exit(1)

print(f"✓ First image: {images[0].name}")

# Test EasyOCR import
try:
    import easyocr
    print("✓ EasyOCR imported successfully")
except ImportError as e:
    print(f"❌ Failed to import EasyOCR: {e}")
    sys.exit(1)

# Test OpenCV import
try:
    import cv2
    print("✓ OpenCV imported successfully")
except ImportError as e:
    print(f"❌ Failed to import OpenCV: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("TESTING OCR ON SINGLE PRESCRIPTION")
print("="*80)

# Initialize reader (this will download models on first run)
print("\nInitializing EasyOCR reader (may download models ~350MB on first run)...")
reader = easyocr.Reader(['en'], gpu=False, verbose=True)
print("✓ EasyOCR reader initialized")

# Test on first prescription
test_image = str(images[0])
print(f"\nProcessing: {images[0].name}")

# Read and extract text
results = reader.readtext(test_image)

print(f"\n{'='*80}")
print(f"RESULTS")
print(f"{'='*80}")
print(f"Text blocks extracted: {len(results)}")
print(f"\nExtracted text:")
print("-" * 80)

for i, (bbox, text, confidence) in enumerate(results, 1):
    print(f"{i}. {text} (confidence: {confidence:.2%})")

print("-" * 80)

# Calculate average confidence
if results:
    avg_conf = sum(conf for _, _, conf in results) / len(results)
    print(f"\nAverage confidence: {avg_conf:.2%}")
else:
    print("\n⚠️  No text detected")

print("\n✓ OCR test complete!")
print("\nTo process all prescriptions, run:")
print("python prescription_ocr/prescription_ocr.py \"datasets/handwritten_pages_jpg (1)/handwritten_pages_jpg\"")
