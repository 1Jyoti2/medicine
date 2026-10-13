"""
Prescription OCR - Extract text from handwritten prescriptions
Uses EasyOCR for handwriting recognition
"""
import os
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import easyocr
from datetime import datetime
import argparse


class PrescriptionOCR:
    """
    OCR system for extracting text from handwritten medical prescriptions
    """
    
    def __init__(self, languages=['en'], gpu=False, verbose=True):
        """
        Initialize OCR reader
        
        Args:
            languages: List of language codes (default: ['en'])
            gpu: Use GPU if available
            verbose: Print progress
        """
        self.verbose = verbose
        if self.verbose:
            print("Initializing EasyOCR...")
            print(f"Languages: {languages}")
            print(f"GPU: {gpu}")
        
        # Initialize EasyOCR reader
        self.reader = easyocr.Reader(languages, gpu=gpu)
        
        if self.verbose:
            print("✓ EasyOCR initialized successfully")
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for better OCR results
        
        Args:
            image_path: Path to prescription image
            
        Returns:
            Preprocessed image (numpy array)
        """
        # Read image
        img = cv2.imread(str(image_path))
        
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Optional: Dilation and erosion to remove noise
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return processed
    
    def extract_text(self, image_path, preprocess=True):
        """
        Extract text from prescription image
        
        Args:
            image_path: Path to prescription image
            preprocess: Apply preprocessing
            
        Returns:
            Dictionary with extracted text and metadata
        """
        if self.verbose:
            print(f"\nProcessing: {Path(image_path).name}")
        
        # Preprocess if enabled
        if preprocess:
            image = self.preprocess_image(image_path)
        else:
            image = cv2.imread(str(image_path))
        
        # Extract text using EasyOCR
        results = self.reader.readtext(image)
        
        # Parse results
        extracted_data = {
            'filename': Path(image_path).name,
            'timestamp': datetime.now().isoformat(),
            'text_blocks': [],
            'full_text': '',
            'confidence_scores': []
        }
        
        full_text_lines = []
        
        for detection in results:
            bbox, text, confidence = detection
            
            extracted_data['text_blocks'].append({
                'text': text,
                'confidence': float(confidence),
                'bbox': [[int(x), int(y)] for x, y in bbox]
            })
            
            extracted_data['confidence_scores'].append(float(confidence))
            full_text_lines.append(text)
        
        # Combine all text
        extracted_data['full_text'] = '\n'.join(full_text_lines)
        extracted_data['average_confidence'] = float(np.mean(extracted_data['confidence_scores'])) if extracted_data['confidence_scores'] else 0.0
        extracted_data['total_blocks'] = len(results)
        
        if self.verbose:
            print(f"  Extracted {len(results)} text blocks")
            print(f"  Average confidence: {extracted_data['average_confidence']:.2%}")
        
        return extracted_data
    
    def process_dataset(self, dataset_dir, output_dir, preprocess=True):
        """
        Process all prescriptions in a dataset
        
        Args:
            dataset_dir: Directory containing prescription images
            output_dir: Directory to save extracted data
            preprocess: Apply preprocessing
            
        Returns:
            Summary statistics
        """
        dataset_dir = Path(dataset_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all image files
        image_extensions = ['.jpg', '.jpeg', '.png']
        image_files = []
        for ext in image_extensions:
            image_files.extend(list(dataset_dir.glob(f'*{ext}')))
            image_files.extend(list(dataset_dir.glob(f'*{ext.upper()}')))
        
        if self.verbose:
            print(f"\n{'='*80}")
            print("PROCESSING PRESCRIPTION DATASET")
            print(f"{'='*80}")
            print(f"Dataset directory: {dataset_dir}")
            print(f"Output directory: {output_dir}")
            print(f"Total images: {len(image_files)}")
            print(f"Preprocessing: {preprocess}")
        
        # Process each image
        results = []
        successful = 0
        failed = 0
        
        for i, image_path in enumerate(image_files, 1):
            try:
                if self.verbose:
                    print(f"\n[{i}/{len(image_files)}] ", end='')
                
                # Extract text
                extracted_data = self.extract_text(image_path, preprocess=preprocess)
                results.append(extracted_data)
                
                # Save individual result
                output_file = output_dir / f"{Path(image_path).stem}_extracted.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(extracted_data, f, indent=2, ensure_ascii=False)
                
                successful += 1
                
            except Exception as e:
                if self.verbose:
                    print(f"  ❌ Error: {str(e)}")
                failed += 1
        
        # Save combined results
        combined_output = output_dir / 'all_prescriptions_extracted.json'
        with open(combined_output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Generate summary statistics
        summary = {
            'total_images': len(image_files),
            'successful': successful,
            'failed': failed,
            'success_rate': successful / len(image_files) if len(image_files) > 0 else 0,
            'total_text_blocks': sum(r['total_blocks'] for r in results),
            'average_confidence': float(np.mean([r['average_confidence'] for r in results])) if results else 0.0,
            'average_blocks_per_image': sum(r['total_blocks'] for r in results) / len(results) if results else 0,
            'processing_date': datetime.now().isoformat()
        }
        
        # Save summary
        summary_file = output_dir / 'processing_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        if self.verbose:
            print(f"\n{'='*80}")
            print("PROCESSING COMPLETE")
            print(f"{'='*80}")
            print(f"Successful: {successful}/{len(image_files)}")
            print(f"Failed: {failed}/{len(image_files)}")
            print(f"Average confidence: {summary['average_confidence']:.2%}")
            print(f"Total text blocks: {summary['total_text_blocks']}")
            print(f"Average blocks per image: {summary['average_blocks_per_image']:.1f}")
            print(f"\nResults saved to: {output_dir}")
        
        return summary


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Extract text from handwritten prescriptions using OCR"
    )
    
    parser.add_argument(
        'dataset_dir',
        type=str,
        help='Directory containing prescription images'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='prescription_ocr/extracted_text',
        help='Output directory for extracted text (default: prescription_ocr/extracted_text)'
    )
    
    parser.add_argument(
        '--languages',
        type=str,
        nargs='+',
        default=['en'],
        help='OCR languages (default: en)'
    )
    
    parser.add_argument(
        '--gpu',
        action='store_true',
        help='Use GPU for OCR'
    )
    
    parser.add_argument(
        '--no-preprocess',
        action='store_true',
        help='Skip image preprocessing'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize OCR
        ocr = PrescriptionOCR(
            languages=args.languages,
            gpu=args.gpu,
            verbose=True
        )
        
        # Process dataset
        summary = ocr.process_dataset(
            dataset_dir=args.dataset_dir,
            output_dir=args.output_dir,
            preprocess=not args.no_preprocess
        )
        
        return 0
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
