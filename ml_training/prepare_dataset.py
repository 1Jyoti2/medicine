"""
Main Dataset Preprocessing Script
Orchestrates the complete preprocessing pipeline:
1. Validate images
2. Detect duplicates
3. Compute statistics
4. Split dataset into train/val/test
5. Generate reports and class mappings
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import argparse
import json
from datetime import datetime

from config.dataset_config import (
    DATASET_RAW_DIR,
    DATASET_PROCESSED_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    CLASS_MAPPING_FILE,
    DATASET_STATS_FILE,
    CORRUPTED_FILES_LOG,
    DUPLICATE_FILES_LOG,
    PREPROCESSING_LOG,
    ensure_directories,
)

from utils.image_validator import ImageValidator
from utils.duplicate_detector import DuplicateDetector
from utils.dataset_stats import DatasetStatistics
from utils.dataset_splitter import DatasetSplitter


class DatasetPreprocessor:
    """
    Main preprocessing pipeline orchestrator
    """
    
    def __init__(self, source_dir: Path = DATASET_RAW_DIR,
                 output_dir: Path = DATASET_PROCESSED_DIR,
                 skip_validation: bool = False,
                 skip_duplicate_check: bool = False,
                 resize_images: bool = False,
                 verbose: bool = True):
        """
        Initialize preprocessor
        
        Args:
            source_dir: Source dataset directory
            output_dir: Output directory for processed dataset
            skip_validation: Skip image validation step
            skip_duplicate_check: Skip duplicate detection step
            resize_images: Resize images during splitting
            verbose: Print detailed progress
        """
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.skip_validation = skip_validation
        self.skip_duplicate_check = skip_duplicate_check
        self.resize_images = resize_images
        self.verbose = verbose
        
        # Results storage
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'source_dir': str(source_dir),
            'output_dir': str(output_dir),
            'steps_completed': [],
            'validation': None,
            'duplicates': None,
            'statistics': None,
            'split': None,
        }
        
        # Ensure output directories exist
        ensure_directories()
    
    def run(self):
        """
        Execute the complete preprocessing pipeline
        """
        print("\n" + "="*80)
        print(" DATASET PREPROCESSING PIPELINE")
        print("="*80)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Source: {self.source_dir}")
        print(f"Output: {self.output_dir}")
        print("="*80)
        
        # Check if source directory exists
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {self.source_dir}")
        
        valid_files = None
        
        # Step 1: Image Validation
        if not self.skip_validation:
            print(f"\n{'>'*80}")
            print("STEP 1/5: IMAGE VALIDATION")
            print(f"{'>'*80}")
            
            validator = ImageValidator(verbose=self.verbose)
            validation_results = validator.validate_dataset(self.source_dir)
            
            # Save invalid files report
            validator.save_invalid_files_report(CORRUPTED_FILES_LOG)
            
            # Get valid files for next steps
            valid_files = validator.get_valid_files()
            
            self.results['validation'] = validation_results
            self.results['steps_completed'].append('validation')
            
            # Check if we have enough valid files
            if validation_results['total_valid'] == 0:
                raise ValueError("No valid images found in dataset!")
            
            print(f"\n✓ Validation complete: {validation_results['total_valid']} valid images")
        
        # Step 2: Duplicate Detection
        if not self.skip_duplicate_check:
            print(f"\n{'>'*80}")
            print("STEP 2/5: DUPLICATE DETECTION")
            print(f"{'>'*80}")
            
            detector = DuplicateDetector(verbose=self.verbose)
            
            if valid_files:
                # Use only valid files
                valid_file_paths = [Path(f) for f in valid_files]
                duplicate_results = detector.detect_duplicates(valid_file_paths)
            else:
                # Use all files
                duplicate_results = detector.detect_duplicates_in_dataset(self.source_dir)
            
            # Save duplicate report
            detector.save_duplicate_report(DUPLICATE_FILES_LOG)
            
            # Update valid files to exclude duplicates if needed
            # (Currently we keep all files, but log the duplicates)
            
            self.results['duplicates'] = duplicate_results
            self.results['steps_completed'].append('duplicate_detection')
            
            print(f"\n✓ Duplicate detection complete: {duplicate_results['duplicate_pairs']} duplicate pairs found")
        
        # Step 3: Dataset Statistics
        print(f"\n{'>'*80}")
        print("STEP 3/5: DATASET STATISTICS")
        print(f"{'>'*80}")
        
        stats = DatasetStatistics(verbose=self.verbose)
        statistics_results = stats.compute_statistics(self.source_dir, valid_files)
        
        # Save statistics
        stats.save_statistics(DATASET_STATS_FILE)
        
        # Save class mapping
        stats.save_class_mapping(CLASS_MAPPING_FILE)
        
        self.results['statistics'] = stats.get_summary()
        self.results['steps_completed'].append('statistics')
        
        print(f"\n✓ Statistics complete: {statistics_results['total_classes']} classes, {statistics_results['total_images']} images")
        
        # Step 4: Dataset Splitting
        print(f"\n{'>'*80}")
        print("STEP 4/5: DATASET SPLITTING")
        print(f"{'>'*80}")
        
        splitter = DatasetSplitter(verbose=self.verbose)
        split_results = splitter.split_dataset(
            source_dir=self.source_dir,
            output_dir=self.output_dir,
            valid_files=valid_files,
            resize=self.resize_images
        )
        
        # Save split info
        split_info_path = self.output_dir / "split_info.json"
        splitter.save_split_info(split_info_path)
        
        self.results['split'] = split_results
        self.results['steps_completed'].append('splitting')
        
        print(f"\n✓ Splitting complete: Train={split_results['total_train']}, Val={split_results['total_val']}, Test={split_results['total_test']}")
        
        # Step 5: Generate Final Report
        print(f"\n{'>'*80}")
        print("STEP 5/5: GENERATING FINAL REPORT")
        print(f"{'>'*80}")
        
        self._generate_final_report()
        self.results['steps_completed'].append('final_report')
        
        # Print completion summary
        self._print_completion_summary()
    
    def _generate_final_report(self):
        """Generate comprehensive preprocessing report"""
        report_path = PREPROCESSING_LOG
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("DATASET PREPROCESSING REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Generated: {self.results['timestamp']}\n")
            f.write(f"Source directory: {self.results['source_dir']}\n")
            f.write(f"Output directory: {self.results['output_dir']}\n\n")
            
            # Validation results
            if self.results['validation']:
                f.write("-"*80 + "\n")
                f.write("IMAGE VALIDATION\n")
                f.write("-"*80 + "\n")
                val = self.results['validation']
                f.write(f"Total images processed: {val['total']}\n")
                f.write(f"Valid images: {val['total_valid']} ({val['valid_percentage']:.1f}%)\n")
                f.write(f"Invalid images: {val['total_invalid']}\n")
                if val['total_invalid'] > 0:
                    f.write(f"  Details:\n")
                    for key, value in val['details'].items():
                        if value > 0:
                            f.write(f"    - {key.replace('_', ' ').title()}: {value}\n")
                f.write(f"\nSee {CORRUPTED_FILES_LOG} for details.\n\n")
            
            # Duplicate detection results
            if self.results['duplicates']:
                f.write("-"*80 + "\n")
                f.write("DUPLICATE DETECTION\n")
                f.write("-"*80 + "\n")
                dup = self.results['duplicates']
                f.write(f"Total images analyzed: {dup['total_images']}\n")
                f.write(f"Duplicate pairs found: {dup['duplicate_pairs']}\n")
                f.write(f"Files involved in duplicates: {dup['duplicate_files']}\n")
                f.write(f"Unique images: {dup['unique_images']}\n")
                f.write(f"\nSee {DUPLICATE_FILES_LOG} for details.\n\n")
            
            # Statistics results
            if self.results['statistics']:
                f.write("-"*80 + "\n")
                f.write("DATASET STATISTICS\n")
                f.write("-"*80 + "\n")
                stat = self.results['statistics']
                f.write(f"Total classes: {stat['total_classes']}\n")
                f.write(f"Total images: {stat['total_images']}\n")
                f.write(f"\nClass distribution:\n")
                for class_name in stat['classes']:
                    count = stat['class_counts'][class_name]
                    percentage = stat['class_distribution'][class_name]
                    f.write(f"  - {class_name:<30} {count:>6} ({percentage:>5.1f}%)\n")
                
                if stat['imbalanced_classes']:
                    f.write(f"\n⚠️  Imbalanced classes:\n")
                    for class_name in stat['imbalanced_classes']:
                        f.write(f"  - {class_name}\n")
                
                f.write(f"\nSee {DATASET_STATS_FILE} for complete statistics.\n\n")
            
            # Split results
            if self.results['split']:
                f.write("-"*80 + "\n")
                f.write("DATASET SPLITTING\n")
                f.write("-"*80 + "\n")
                split = self.results['split']
                f.write(f"Training set: {split['total_train']} images ({split['train_ratio']*100:.0f}%)\n")
                f.write(f"Validation set: {split['total_val']} images ({split['val_ratio']*100:.0f}%)\n")
                f.write(f"Test set: {split['total_test']} images ({split['test_ratio']*100:.0f}%)\n")
                f.write(f"Random seed: {split['random_seed']}\n")
                f.write(f"\nOutput directory: {split['output_dir']}\n\n")
            
            f.write("="*80 + "\n")
            f.write("PREPROCESSING COMPLETE\n")
            f.write("="*80 + "\n")
            f.write(f"Steps completed: {', '.join(self.results['steps_completed'])}\n")
            f.write(f"\nClass mapping saved to: {CLASS_MAPPING_FILE}\n")
            f.write(f"Statistics saved to: {DATASET_STATS_FILE}\n")
            f.write(f"Processed dataset: {self.results['output_dir']}\n")
        
        if self.verbose:
            print(f"\n✓ Final report saved to: {report_path}")
    
    def _print_completion_summary(self):
        """Print preprocessing completion summary"""
        print("\n" + "="*80)
        print(" PREPROCESSING COMPLETE")
        print("="*80)
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nSteps completed: {len(self.results['steps_completed'])}/5")
        for step in self.results['steps_completed']:
            print(f"  ✓ {step.replace('_', ' ').title()}")
        
        print(f"\n{'='*80}")
        print("OUTPUT FILES")
        print(f"{'='*80}")
        print(f"Processed dataset:     {self.output_dir}")
        print(f"  - Train:             {self.output_dir / 'train'}")
        print(f"  - Validation:        {self.output_dir / 'val'}")
        print(f"  - Test:              {self.output_dir / 'test'}")
        print(f"\nClass mapping:         {CLASS_MAPPING_FILE}")
        print(f"Dataset statistics:    {DATASET_STATS_FILE}")
        print(f"Preprocessing log:     {PREPROCESSING_LOG}")
        
        if not self.skip_validation:
            print(f"Corrupted files log:   {CORRUPTED_FILES_LOG}")
        
        if not self.skip_duplicate_check:
            print(f"Duplicate files log:   {DUPLICATE_FILES_LOG}")
        
        print(f"\n{'='*80}")
        print("NEXT STEPS")
        print(f"{'='*80}")
        print("1. Review the preprocessing reports for any issues")
        print("2. Train your model using the processed dataset")
        print("3. Use the class mapping file for prediction decoding")
        print("\nExample:")
        print("  python scripts/train_model.py")
        print("="*80 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Preprocess leaf dataset for ML training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full preprocessing pipeline
  python prepare_dataset.py
  
  # Skip validation (if already validated)
  python prepare_dataset.py --skip-validation
  
  # Skip duplicate check
  python prepare_dataset.py --skip-duplicate-check
  
  # Resize images during splitting
  python prepare_dataset.py --resize
  
  # Custom source and output directories
  python prepare_dataset.py --source /path/to/source --output /path/to/output
        """
    )
    
    parser.add_argument(
        '--source',
        type=str,
        default=str(DATASET_RAW_DIR),
        help=f'Source dataset directory (default: {DATASET_RAW_DIR})'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=str(DATASET_PROCESSED_DIR),
        help=f'Output directory for processed dataset (default: {DATASET_PROCESSED_DIR})'
    )
    
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip image validation step'
    )
    
    parser.add_argument(
        '--skip-duplicate-check',
        action='store_true',
        help='Skip duplicate detection step'
    )
    
    parser.add_argument(
        '--resize',
        action='store_true',
        help='Resize images during splitting'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        preprocessor = DatasetPreprocessor(
            source_dir=args.source,
            output_dir=args.output,
            skip_validation=args.skip_validation,
            skip_duplicate_check=args.skip_duplicate_check,
            resize_images=args.resize,
            verbose=not args.quiet
        )
        
        preprocessor.run()
        
        return 0
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
