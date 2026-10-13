# Prescription OCR Pipeline

## Overview
Optical Character Recognition (OCR) system for handwritten medical prescriptions.

## Dataset
- **Location:** `datasets/handwritten_pages_jpg (1)/handwritten_pages_jpg/`
- **Total Images:** 30 prescription images
- **Format:** JPG
- **Content:** Handwritten medical prescriptions

## Approach

### Option 1: EasyOCR (Recommended for Handwriting)
- Pre-trained model with handwriting support
- Multiple language support
- Good for medical terminology
- Easy to use

### Option 2: TrOCR (Transformer-based)
- Microsoft's transformer-based OCR
- Excellent for handwritten text
- Requires more computational resources

### Option 3: Tesseract OCR
- Traditional OCR engine
- Less accurate for handwriting
- Good for printed text only

## Implementation Status
🔄 In Progress - Setting up pipeline

## Next Steps
1. Analyze prescription image quality
2. Choose OCR approach
3. Implement preprocessing
4. Extract text from prescriptions
5. Structure extracted data
6. Create API endpoint
