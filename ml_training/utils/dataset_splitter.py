"""
Dataset Splitting Utility
Stratified split of dataset into train/validation/test sets without data leakage
"""
import os
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import random
import numpy as np
from PIL import Image

from config.dataset_config import (
    TRAIN_RATIO,
    VAL_RATIO,
    TEST_RATIO,
    RANDOM_SEED,
    IMAGE_SIZE,
)


class DatasetSplitter:
    """
    Split dataset into train/val/test with stratification
    """
    
    def __init__(self, train_ratio: float = TRAIN_RATIO,
                 val_ratio: float = VAL_RATIO,
                 test_ratio: float = TEST_RATIO,
                 random_seed: int = RANDOM_SEED,
                 verbose: bool = True):
        """
        Initialize dataset splitter
        
        Args:
            train_ratio: Proportion for training set
            val_ratio: Proportion for validation set
            test_ratio: Proportion for test set
            random_seed: Random seed for reproducibility
            verbose: Print splitting progress
        """
        # Validate ratios
        total_ratio = train_ratio + val_ratio + test_ratio
        if not np.isclose(total_ratio, 1.0):
            raise ValueError(f"Ratios must sum to 1.0, got {total_ratio}")
        
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.random_seed = random_seed
        self.verbose = verbose
        
        # Set random seeds for reproducibility
        random.seed(random_seed)
        np.random.seed(random_seed)
        
        self.split_info = {}
    
    def split_dataset(self, source_dir: Path, output_dir: Path,
                     valid_files: List[str] = None,
                     resize: bool = False,
                     target_size: Tuple[int, int] = IMAGE_SIZE) -> Dict:
        """
        Split dataset into train/val/test sets
        
        Args:
            source_dir: Source dataset directory with class subdirectories
            output_dir: Output directory for split dataset
            valid_files: Optional list of valid files to include
            resize: Whether to resize images during split
            target_size: Target size for resizing
            
        Returns:
            Dictionary with split statistics
        """
        if self.verbose:
            print(f"\n{'='*80}")
            print("DATASET SPLITTING")
            print(f"{'='*80}")
            print(f"Source: {source_dir}")
            print(f"Output: {output_dir}")
            print(f"Split ratios: Train={self.train_ratio}, Val={self.val_ratio}, Test={self.test_ratio}")
            print(f"Random seed: {self.random_seed}")
            print(f"Resize images: {resize} {f'to {target_size}' if resize else ''}")
        
        # Create output directories
        train_dir = output_dir / "train"
        val_dir = output_dir / "val"
        test_dir = output_dir / "test"
        
        for split_dir in [train_dir, val_dir, test_dir]:
            split_dir.mkdir(parents=True, exist_ok=True)
        
        # Get valid files set
        valid_files_set = set(valid_files) if valid_files else None
        
        # Process each class
        class_splits = {}
        total_train = 0
        total_val = 0
        total_test = 0
        
        for class_dir in sorted(source_dir.iterdir()):
            if not class_dir.is_dir():
                continue
            
            class_name = class_dir.name
            
            if self.verbose:
                print(f"\nProcessing class: {class_name}")
            
            # Get all image files (case-insensitive, avoid duplicates)
            unique_files = set()
            for ext in ['.jpg', '.jpeg', '.png']:
                for file in class_dir.glob(f"*{ext}"):
                    unique_files.add(file)
                for file in class_dir.glob(f"*{ext.upper()}"):
                    unique_files.add(file)
            image_files = list(unique_files)
            
            # Filter by valid files
            if valid_files_set:
                image_files = [f for f in image_files if str(f) in valid_files_set]
            
            # Shuffle files
            image_files = list(image_files)
            random.shuffle(image_files)
            
            # Calculate split indices
            n_total = len(image_files)
            n_train = int(n_total * self.train_ratio)
            n_val = int(n_total * self.val_ratio)
            n_test = n_total - n_train - n_val  # Remaining go to test
            
            # Split files
            train_files = image_files[:n_train]
            val_files = image_files[n_train:n_train + n_val]
            test_files = image_files[n_train + n_val:]
            
            if self.verbose:
                print(f"  Total: {n_total} | Train: {n_train} | Val: {n_val} | Test: {n_test}")
            
            # Copy files to split directories
            class_splits[class_name] = {
                'total': n_total,
                'train': n_train,
                'val': n_val,
                'test': n_test
            }
            
            self._copy_files(train_files, train_dir / class_name, resize, target_size)
            self._copy_files(val_files, val_dir / class_name, resize, target_size)
            self._copy_files(test_files, test_dir / class_name, resize, target_size)
            
            total_train += n_train
            total_val += n_val
            total_test += n_test
        
        # Store split info
        self.split_info = {
            'source_dir': str(source_dir),
            'output_dir': str(output_dir),
            'train_ratio': self.train_ratio,
            'val_ratio': self.val_ratio,
            'test_ratio': self.test_ratio,
            'random_seed': self.random_seed,
            'resize': resize,
            'target_size': target_size if resize else None,
            'total_train': total_train,
            'total_val': total_val,
            'total_test': total_test,
            'total': total_train + total_val + total_test,
            'class_splits': class_splits,
        }
        
        if self.verbose:
            self._print_summary()
        
        return self.split_info
    
    def _copy_files(self, files: List[Path], dest_dir: Path,
                   resize: bool, target_size: Tuple[int, int]):
        """
        Copy files to destination directory with optional resizing
        
        Args:
            files: List of source file paths
            dest_dir: Destination directory
            resize: Whether to resize images
            target_size: Target size for resizing
        """
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path in files:
            dest_path = dest_dir / file_path.name
            
            if resize:
                try:
                    # Open, resize, and save image
                    with Image.open(file_path) as img:
                        # Convert to RGB if needed
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Resize
                        img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                        
                        # Save
                        img_resized.save(dest_path, quality=95)
                
                except Exception as e:
                    if self.verbose:
                        print(f"    Warning: Could not resize {file_path.name}: {e}")
                    # Fallback to copy
                    shutil.copy2(file_path, dest_path)
            else:
                # Direct copy
                shutil.copy2(file_path, dest_path)
    
    def _print_summary(self):
        """Print dataset splitting summary"""
        print(f"\n{'='*80}")
        print("DATASET SPLITTING SUMMARY")
        print(f"{'='*80}")
        
        print(f"\nOverall Split:")
        print(f"  Training set:     {self.split_info['total_train']:6d} images ({self.split_info['total_train']/self.split_info['total']*100:.1f}%)")
        print(f"  Validation set:   {self.split_info['total_val']:6d} images ({self.split_info['total_val']/self.split_info['total']*100:.1f}%)")
        print(f"  Test set:         {self.split_info['total_test']:6d} images ({self.split_info['total_test']/self.split_info['total']*100:.1f}%)")
        print(f"  Total:            {self.split_info['total']:6d} images")
        
        print(f"\n{'='*80}")
        print("PER-CLASS SPLIT")
        print(f"{'='*80}")
        print(f"{'Class':<30} {'Total':>8} {'Train':>8} {'Val':>8} {'Test':>8}")
        print(f"{'-'*30} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
        
        for class_name, splits in self.split_info['class_splits'].items():
            print(f"{class_name:<30} {splits['total']:>8} {splits['train']:>8} {splits['val']:>8} {splits['test']:>8}")
        
        print(f"\n✓ Dataset successfully split into train/val/test sets")
        print(f"  Output directory: {self.split_info['output_dir']}")
    
    def get_summary(self) -> Dict:
        """
        Get split summary
        
        Returns:
            Dictionary with split statistics
        """
        return self.split_info
    
    def save_split_info(self, output_path: Path):
        """
        Save split information to JSON file
        
        Args:
            output_path: Path to output JSON file
        """
        import json
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.split_info, f, indent=2)
        
        if self.verbose:
            print(f"\nSplit info saved to: {output_path}")


if __name__ == "__main__":
    # Test dataset splitting
    from config.dataset_config import DATASET_RAW_DIR, DATASET_PROCESSED_DIR
    
    splitter = DatasetSplitter(verbose=True)
    results = splitter.split_dataset(
        source_dir=DATASET_RAW_DIR,
        output_dir=DATASET_PROCESSED_DIR,
        resize=False  # Set to True to resize during split
    )
    
    # Save split info
    split_info_path = DATASET_PROCESSED_DIR / "split_info.json"
    splitter.save_split_info(split_info_path)
    
    print("\nDataset splitting complete!")
