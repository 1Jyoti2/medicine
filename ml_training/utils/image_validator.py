"""
Image Validation Utility
Validates image files for corruption, format, size, and integrity
"""
import os
from pathlib import Path
from typing import List, Tuple, Dict
from PIL import Image
import numpy as np

from config.dataset_config import (
    SUPPORTED_FORMATS,
    MIN_IMAGE_SIZE,
    MAX_IMAGE_SIZE,
    MIN_FILE_SIZE,
    MAX_FILE_SIZE,
)


class ImageValidator:
    """
    Validates image files for ML dataset preprocessing
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize validator
        
        Args:
            verbose: Print validation progress
        """
        self.verbose = verbose
        self.validation_results = {
            'valid': [],
            'corrupted': [],
            'wrong_format': [],
            'too_small': [],
            'too_large': [],
            'file_too_small': [],
            'file_too_large': [],
            'cannot_open': [],
        }
    
    def validate_image(self, image_path: Path) -> Tuple[bool, str]:
        """
        Validate a single image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check if file exists
            if not image_path.exists():
                return False, "File does not exist"
            
            # Check file extension
            if image_path.suffix.lower() not in SUPPORTED_FORMATS:
                return False, f"Unsupported format: {image_path.suffix}"
            
            # Check file size
            file_size = image_path.stat().st_size
            if file_size < MIN_FILE_SIZE:
                return False, f"File too small: {file_size} bytes"
            if file_size > MAX_FILE_SIZE:
                return False, f"File too large: {file_size} bytes"
            
            # Try to open and validate image
            try:
                with Image.open(image_path) as img:
                    # Verify it's a valid image
                    img.verify()
                
                # Re-open for further checks (verify() closes the file)
                with Image.open(image_path) as img:
                    # Check dimensions
                    width, height = img.size
                    
                    if width < MIN_IMAGE_SIZE[0] or height < MIN_IMAGE_SIZE[1]:
                        return False, f"Image too small: {width}x{height}"
                    
                    if width > MAX_IMAGE_SIZE[0] or height > MAX_IMAGE_SIZE[1]:
                        return False, f"Image too large: {width}x{height}"
                    
                    # Check if image can be converted to RGB
                    try:
                        img.convert('RGB')
                    except Exception as e:
                        return False, f"Cannot convert to RGB: {str(e)}"
                    
                    # Try to load image data (catches some corruptions)
                    try:
                        img.load()
                    except Exception as e:
                        return False, f"Cannot load image data: {str(e)}"
                
                return True, "Valid"
            
            except Exception as e:
                return False, f"Cannot open image: {str(e)}"
        
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def validate_dataset(self, dataset_path: Path) -> Dict:
        """
        Validate all images in a dataset directory
        
        Args:
            dataset_path: Path to dataset directory with class subdirectories
            
        Returns:
            Dictionary with validation results
        """
        if self.verbose:
            print(f"\n{'='*80}")
            print("IMAGE VALIDATION")
            print(f"{'='*80}")
            print(f"Dataset path: {dataset_path}")
        
        # Reset results
        self.validation_results = {
            'valid': [],
            'corrupted': [],
            'wrong_format': [],
            'too_small': [],
            'too_large': [],
            'file_too_small': [],
            'file_too_large': [],
            'cannot_open': [],
        }
        
        # Get all image files (case-insensitive on Windows, avoid duplicates)
        image_files = []
        for class_dir in dataset_path.iterdir():
            if class_dir.is_dir():
                # Use a set to track unique files (handles case-insensitive filesystems)
                unique_files = set()
                for ext in SUPPORTED_FORMATS:
                    for file in class_dir.glob(f"*{ext}"):
                        unique_files.add(file)
                    for file in class_dir.glob(f"*{ext.upper()}"):
                        unique_files.add(file)
                image_files.extend(sorted(unique_files))
        
        total_files = len(image_files)
        
        if self.verbose:
            print(f"Found {total_files} image files to validate")
            print()
        
        # Validate each image
        for idx, image_path in enumerate(image_files, 1):
            is_valid, message = self.validate_image(image_path)
            
            if is_valid:
                self.validation_results['valid'].append(str(image_path))
            else:
                # Categorize error
                if "format" in message.lower():
                    self.validation_results['wrong_format'].append((str(image_path), message))
                elif "too small" in message.lower() and "file" in message.lower():
                    self.validation_results['file_too_small'].append((str(image_path), message))
                elif "too large" in message.lower() and "file" in message.lower():
                    self.validation_results['file_too_large'].append((str(image_path), message))
                elif "too small" in message.lower():
                    self.validation_results['too_small'].append((str(image_path), message))
                elif "too large" in message.lower():
                    self.validation_results['too_large'].append((str(image_path), message))
                elif "cannot open" in message.lower():
                    self.validation_results['cannot_open'].append((str(image_path), message))
                else:
                    self.validation_results['corrupted'].append((str(image_path), message))
            
            # Progress indicator
            if self.verbose and idx % 100 == 0:
                print(f"Validated {idx}/{total_files} images...", end='\r')
        
        if self.verbose:
            print(f"Validated {total_files}/{total_files} images... Done!")
            self._print_summary()
        
        return self.get_summary()
    
    def _print_summary(self):
        """Print validation summary"""
        print(f"\n{'='*80}")
        print("VALIDATION SUMMARY")
        print(f"{'='*80}")
        
        total_valid = len(self.validation_results['valid'])
        total_invalid = sum(
            len(v) if isinstance(v, list) else 0 
            for k, v in self.validation_results.items() 
            if k != 'valid'
        )
        total = total_valid + total_invalid
        
        print(f"[OK] Valid images:        {total_valid:6d} ({total_valid/total*100:.1f}%)")
        print(f"[X]  Invalid images:      {total_invalid:6d} ({total_invalid/total*100:.1f}%)")
        print(f"  Total:               {total:6d}")
        print()
        
        if total_invalid > 0:
            print("Invalid image breakdown:")
            print(f"  - Corrupted:         {len(self.validation_results['corrupted']):6d}")
            print(f"  - Wrong format:      {len(self.validation_results['wrong_format']):6d}")
            print(f"  - Image too small:   {len(self.validation_results['too_small']):6d}")
            print(f"  - Image too large:   {len(self.validation_results['too_large']):6d}")
            print(f"  - File too small:    {len(self.validation_results['file_too_small']):6d}")
            print(f"  - File too large:    {len(self.validation_results['file_too_large']):6d}")
            print(f"  - Cannot open:       {len(self.validation_results['cannot_open']):6d}")
    
    def get_summary(self) -> Dict:
        """
        Get validation summary as dictionary
        
        Returns:
            Dictionary with validation statistics
        """
        total_valid = len(self.validation_results['valid'])
        total_invalid = sum(
            len(v) if isinstance(v, list) else 0 
            for k, v in self.validation_results.items() 
            if k != 'valid'
        )
        
        return {
            'total_valid': total_valid,
            'total_invalid': total_invalid,
            'total': total_valid + total_invalid,
            'valid_percentage': total_valid / (total_valid + total_invalid) * 100 if (total_valid + total_invalid) > 0 else 0,
            'details': {
                'corrupted': len(self.validation_results['corrupted']),
                'wrong_format': len(self.validation_results['wrong_format']),
                'too_small': len(self.validation_results['too_small']),
                'too_large': len(self.validation_results['too_large']),
                'file_too_small': len(self.validation_results['file_too_small']),
                'file_too_large': len(self.validation_results['file_too_large']),
                'cannot_open': len(self.validation_results['cannot_open']),
            }
        }
    
    def get_valid_files(self) -> List[str]:
        """
        Get list of valid image files
        
        Returns:
            List of valid image file paths
        """
        return self.validation_results['valid']
    
    def get_invalid_files(self) -> Dict:
        """
        Get dictionary of invalid files by category
        
        Returns:
            Dictionary of invalid files with error messages
        """
        return {
            k: v for k, v in self.validation_results.items() 
            if k != 'valid' and len(v) > 0
        }
    
    def save_invalid_files_report(self, output_path: Path):
        """
        Save report of invalid files to text file
        
        Args:
            output_path: Path to output file
        """
        invalid_files = self.get_invalid_files()
        
        if not invalid_files or sum(len(v) for v in invalid_files.values()) == 0:
            if self.verbose:
                print("\nNo invalid files to report!")
            return
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("INVALID IMAGE FILES REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            for category, files in invalid_files.items():
                if files:
                    f.write(f"\n{category.upper().replace('_', ' ')} ({len(files)} files)\n")
                    f.write("-" * 80 + "\n")
                    for item in files:
                        if isinstance(item, tuple):
                            file_path, message = item
                            f.write(f"  {file_path}\n")
                            f.write(f"    Error: {message}\n\n")
                        else:
                            f.write(f"  {item}\n\n")
        
        if self.verbose:
            print(f"\nInvalid files report saved to: {output_path}")


if __name__ == "__main__":
    # Test validation
    from config.dataset_config import DATASET_RAW_DIR, CORRUPTED_FILES_LOG
    
    validator = ImageValidator(verbose=True)
    results = validator.validate_dataset(DATASET_RAW_DIR)
    
    # Save report
    validator.save_invalid_files_report(CORRUPTED_FILES_LOG)
    
    print("\nValidation complete!")
