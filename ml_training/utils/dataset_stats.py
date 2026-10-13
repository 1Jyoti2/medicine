"""
Dataset Statistics Utility
Automatically discovers classes and computes comprehensive dataset statistics
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import numpy as np
from PIL import Image

from config.dataset_config import (
    SUPPORTED_FORMATS,
    MIN_SAMPLES_PER_CLASS,
    CLASS_IMBALANCE_THRESHOLD,
)


class DatasetStatistics:
    """
    Compute and display comprehensive dataset statistics
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize statistics collector
        
        Args:
            verbose: Print statistics
        """
        self.verbose = verbose
        self.stats = {
            'classes': {},
            'total_images': 0,
            'class_distribution': {},
            'image_dimensions': [],
            'file_sizes': [],
        }
    
    def discover_classes(self, dataset_path: Path) -> List[str]:
        """
        Automatically discover class names from directory structure
        
        Args:
            dataset_path: Path to dataset directory
            
        Returns:
            List of class names (sorted alphabetically)
        """
        classes = []
        
        for item in dataset_path.iterdir():
            if item.is_dir():
                classes.append(item.name)
        
        classes.sort()  # Sort alphabetically for consistency
        
        if self.verbose:
            print(f"\n{'='*80}")
            print("CLASS DISCOVERY")
            print(f"{'='*80}")
            print(f"Dataset path: {dataset_path}")
            print(f"Discovered {len(classes)} classes:")
            for idx, class_name in enumerate(classes, 1):
                print(f"  {idx}. {class_name}")
        
        return classes
    
    def count_images_per_class(self, dataset_path: Path, 
                               valid_files: List[str] = None) -> Dict[str, int]:
        """
        Count number of images in each class
        
        Args:
            dataset_path: Path to dataset directory
            valid_files: Optional list of valid file paths (from validation)
            
        Returns:
            Dictionary mapping class name to image count
        """
        class_counts = {}
        valid_files_set = set(valid_files) if valid_files else None
        
        for class_dir in dataset_path.iterdir():
            if class_dir.is_dir():
                class_name = class_dir.name
                
                # Count image files (case-insensitive, avoid duplicates)
                unique_files = set()
                for ext in SUPPORTED_FORMATS:
                    for file in class_dir.glob(f"*{ext}"):
                        unique_files.add(file)
                    for file in class_dir.glob(f"*{ext.upper()}"):
                        unique_files.add(file)
                image_files = list(unique_files)
                
                # Filter by valid files if provided
                if valid_files_set:
                    image_files = [f for f in image_files if str(f) in valid_files_set]
                
                class_counts[class_name] = len(image_files)
        
        return class_counts
    
    def compute_statistics(self, dataset_path: Path, 
                          valid_files: List[str] = None) -> Dict:
        """
        Compute comprehensive dataset statistics
        
        Args:
            dataset_path: Path to dataset directory
            valid_files: Optional list of valid file paths
            
        Returns:
            Dictionary with all statistics
        """
        if self.verbose:
            print(f"\n{'='*80}")
            print("COMPUTING DATASET STATISTICS")
            print(f"{'='*80}")
        
        # Discover classes
        classes = self.discover_classes(dataset_path)
        
        # Count images per class
        class_counts = self.count_images_per_class(dataset_path, valid_files)
        
        # Compute statistics for each class
        class_stats = {}
        all_dimensions = []
        all_file_sizes = []
        valid_files_set = set(valid_files) if valid_files else None
        
        for class_name in classes:
            class_dir = dataset_path / class_name
            
            # Get image files (case-insensitive, avoid duplicates)
            unique_files = set()
            for ext in SUPPORTED_FORMATS:
                for file in class_dir.glob(f"*{ext}"):
                    unique_files.add(file)
                for file in class_dir.glob(f"*{ext.upper()}"):
                    unique_files.add(file)
            image_files = list(unique_files)
            
            # Filter by valid files
            if valid_files_set:
                image_files = [f for f in image_files if str(f) in valid_files_set]
            
            # Compute statistics for this class
            dimensions = []
            file_sizes = []
            
            for img_path in image_files:
                try:
                    # Get file size
                    file_size = img_path.stat().st_size
                    file_sizes.append(file_size)
                    all_file_sizes.append(file_size)
                    
                    # Get image dimensions
                    with Image.open(img_path) as img:
                        width, height = img.size
                        dimensions.append((width, height))
                        all_dimensions.append((width, height))
                
                except Exception as e:
                    if self.verbose:
                        print(f"Warning: Could not process {img_path}: {e}")
            
            # Store class statistics
            class_stats[class_name] = {
                'count': len(image_files),
                'dimensions': dimensions,
                'file_sizes': file_sizes,
                'avg_width': np.mean([d[0] for d in dimensions]) if dimensions else 0,
                'avg_height': np.mean([d[1] for d in dimensions]) if dimensions else 0,
                'avg_file_size': np.mean(file_sizes) if file_sizes else 0,
            }
        
        # Overall statistics
        total_images = sum(class_counts.values())
        avg_images_per_class = total_images / len(classes) if classes else 0
        
        # Class distribution percentages
        class_distribution = {
            class_name: (count / total_images * 100) if total_images > 0 else 0
            for class_name, count in class_counts.items()
        }
        
        # Check for class imbalance
        imbalanced_classes = []
        for class_name, count in class_counts.items():
            if count < avg_images_per_class * (1 - CLASS_IMBALANCE_THRESHOLD):
                imbalanced_classes.append(class_name)
        
        # Store statistics
        self.stats = {
            'total_classes': len(classes),
            'classes': classes,
            'total_images': total_images,
            'avg_images_per_class': avg_images_per_class,
            'class_counts': class_counts,
            'class_distribution': class_distribution,
            'class_stats': class_stats,
            'imbalanced_classes': imbalanced_classes,
            'overall_stats': {
                'avg_width': np.mean([d[0] for d in all_dimensions]) if all_dimensions else 0,
                'avg_height': np.mean([d[1] for d in all_dimensions]) if all_dimensions else 0,
                'min_width': min([d[0] for d in all_dimensions]) if all_dimensions else 0,
                'max_width': max([d[0] for d in all_dimensions]) if all_dimensions else 0,
                'min_height': min([d[1] for d in all_dimensions]) if all_dimensions else 0,
                'max_height': max([d[1] for d in all_dimensions]) if all_dimensions else 0,
                'avg_file_size': np.mean(all_file_sizes) if all_file_sizes else 0,
                'total_size_mb': sum(all_file_sizes) / (1024 * 1024) if all_file_sizes else 0,
            }
        }
        
        if self.verbose:
            self._print_summary()
        
        return self.stats
    
    def _print_summary(self):
        """Print comprehensive statistics summary"""
        print(f"\n{'='*80}")
        print("DATASET STATISTICS SUMMARY")
        print(f"{'='*80}")
        
        print(f"\nOverall Statistics:")
        print(f"  Total classes:           {self.stats['total_classes']}")
        print(f"  Total images:            {self.stats['total_images']}")
        print(f"  Average per class:       {self.stats['avg_images_per_class']:.1f}")
        print(f"  Total dataset size:      {self.stats['overall_stats']['total_size_mb']:.2f} MB")
        
        print(f"\nImage Dimensions:")
        print(f"  Average:                 {self.stats['overall_stats']['avg_width']:.0f} x {self.stats['overall_stats']['avg_height']:.0f}")
        print(f"  Min:                     {self.stats['overall_stats']['min_width']:.0f} x {self.stats['overall_stats']['min_height']:.0f}")
        print(f"  Max:                     {self.stats['overall_stats']['max_width']:.0f} x {self.stats['overall_stats']['max_height']:.0f}")
        print(f"  Average file size:       {self.stats['overall_stats']['avg_file_size']/1024:.1f} KB")
        
        print(f"\n{'='*80}")
        print("CLASS DISTRIBUTION")
        print(f"{'='*80}")
        print(f"{'Class':<30} {'Count':>10} {'%':>8} {'Status':>15}")
        print(f"{'-'*30} {'-'*10} {'-'*8} {'-'*15}")
        
        for class_name in self.stats['classes']:
            count = self.stats['class_counts'][class_name]
            percentage = self.stats['class_distribution'][class_name]
            
            # Determine status
            if count < MIN_SAMPLES_PER_CLASS:
                status = "⚠️ Too few"
            elif class_name in self.stats['imbalanced_classes']:
                status = "⚠️ Imbalanced"
            else:
                status = "✓ Good"
            
            print(f"{class_name:<30} {count:>10} {percentage:>7.1f}% {status:>15}")
        
        # Warnings
        if self.stats['imbalanced_classes']:
            print(f"\n{'='*80}")
            print("⚠️ CLASS IMBALANCE WARNING")
            print(f"{'='*80}")
            print(f"The following classes have <{int(CLASS_IMBALANCE_THRESHOLD*100)}% of average:")
            for class_name in self.stats['imbalanced_classes']:
                count = self.stats['class_counts'][class_name]
                avg = self.stats['avg_images_per_class']
                print(f"  - {class_name}: {count} images ({count/avg*100:.1f}% of average)")
            print(f"\nRecommendation: Consider data augmentation or collecting more samples.")
        
        # Check minimum samples
        insufficient_classes = [
            name for name, count in self.stats['class_counts'].items()
            if count < MIN_SAMPLES_PER_CLASS
        ]
        
        if insufficient_classes:
            print(f"\n{'='*80}")
            print("❌ INSUFFICIENT SAMPLES WARNING")
            print(f"{'='*80}")
            print(f"The following classes have <{MIN_SAMPLES_PER_CLASS} images:")
            for class_name in insufficient_classes:
                count = self.stats['class_counts'][class_name]
                print(f"  - {class_name}: {count} images (need {MIN_SAMPLES_PER_CLASS - count} more)")
            print(f"\nRecommendation: Collect more samples for these classes.")
    
    def create_class_mapping(self) -> Dict:
        """
        Create class name to index mapping
        
        Returns:
            Dictionary with class_to_idx and idx_to_class mappings
        """
        classes = self.stats['classes']
        
        class_to_idx = {class_name: idx for idx, class_name in enumerate(classes)}
        idx_to_class = {idx: class_name for idx, class_name in enumerate(classes)}
        
        return {
            'num_classes': len(classes),
            'classes': classes,
            'class_to_idx': class_to_idx,
            'idx_to_class': idx_to_class,
        }
    
    def save_statistics(self, output_path: Path):
        """
        Save statistics to JSON file
        
        Args:
            output_path: Path to output JSON file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert numpy types to Python types for JSON serialization
        stats_json = self._convert_to_json_serializable(self.stats)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats_json, f, indent=2)
        
        if self.verbose:
            print(f"\nStatistics saved to: {output_path}")
    
    def save_class_mapping(self, output_path: Path):
        """
        Save class mapping to JSON file
        
        Args:
            output_path: Path to output JSON file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        mapping = self.create_class_mapping()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2)
        
        if self.verbose:
            print(f"Class mapping saved to: {output_path}")
    
    def _convert_to_json_serializable(self, obj):
        """
        Recursively convert numpy types to Python types
        
        Args:
            obj: Object to convert
            
        Returns:
            JSON-serializable object
        """
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: self._convert_to_json_serializable(value) 
                    for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_json_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._convert_to_json_serializable(item) for item in obj)
        else:
            return obj
    
    def get_summary(self) -> Dict:
        """
        Get concise statistics summary
        
        Returns:
            Dictionary with key statistics
        """
        return {
            'total_classes': self.stats['total_classes'],
            'classes': self.stats['classes'],
            'total_images': self.stats['total_images'],
            'class_counts': self.stats['class_counts'],
            'class_distribution': self.stats['class_distribution'],
            'imbalanced_classes': self.stats['imbalanced_classes'],
        }


if __name__ == "__main__":
    # Test statistics computation
    from config.dataset_config import DATASET_RAW_DIR, DATASET_STATS_FILE, CLASS_MAPPING_FILE
    
    stats = DatasetStatistics(verbose=True)
    results = stats.compute_statistics(DATASET_RAW_DIR)
    
    # Save statistics
    stats.save_statistics(DATASET_STATS_FILE)
    stats.save_class_mapping(CLASS_MAPPING_FILE)
    
    print("\nStatistics computation complete!")
