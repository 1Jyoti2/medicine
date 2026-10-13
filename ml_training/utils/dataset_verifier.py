"""
Dataset Verification Utility
Strict verification to detect data leakage, duplicates, and split integrity issues
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import hashlib

class DatasetVerifier:
    """
    Comprehensive dataset verification with strict checks
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize verifier
        
        Args:
            verbose: Print detailed verification output
        """
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.info = []
    
    def compute_file_hash(self, file_path: Path) -> str:
        """
        Compute MD5 hash of file content
        
        Args:
            file_path: Path to file
            
        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def verify_source_dataset(self, source_dir: Path) -> Dict:
        """
        Verify source dataset structure and content
        
        Args:
            source_dir: Path to source dataset
            
        Returns:
            Dictionary with verification results
        """
        if self.verbose:
            print(f"\n{'='*80}")
            print("VERIFYING SOURCE DATASET")
            print(f"{'='*80}")
            print(f"Source: {source_dir}")
        
        if not source_dir.exists():
            self.errors.append(f"Source directory does not exist: {source_dir}")
            return {'valid': False}
        
        # Count classes and images
        classes = []
        class_counts = {}
        total_images = 0
        
        for item in sorted(source_dir.iterdir()):
            if item.is_dir():
                class_name = item.name
                classes.append(class_name)
                
                # Count images (avoid double-counting)
                unique_files = set()
                for ext in ['.jpg', '.jpeg', '.png']:
                    for file in item.glob(f"*{ext}"):
                        unique_files.add(file)
                    for file in item.glob(f"*{ext.upper()}"):
                        unique_files.add(file)
                
                count = len(unique_files)
                class_counts[class_name] = count
                total_images += count
                
                if self.verbose:
                    print(f"  {class_name}: {count} images")
        
        if self.verbose:
            print(f"\nTotal: {len(classes)} classes, {total_images} images")
        
        self.info.append(f"Source dataset: {len(classes)} classes, {total_images} images")
        
        return {
            'valid': True,
            'classes': classes,
            'class_counts': class_counts,
            'total_images': total_images
        }
    
    def verify_split_integrity(self, processed_dir: Path) -> Dict:
        """
        Verify split dataset has no overlap or duplicates
        
        Args:
            processed_dir: Path to processed dataset with train/val/test splits
            
        Returns:
            Dictionary with verification results
        """
        if self.verbose:
            print(f"\n{'='*80}")
            print("VERIFYING SPLIT INTEGRITY")
            print(f"{'='*80}")
        
        train_dir = processed_dir / "train"
        val_dir = processed_dir / "val"
        test_dir = processed_dir / "test"
        
        # Check directories exist
        if not all([train_dir.exists(), val_dir.exists(), test_dir.exists()]):
            self.errors.append("Missing train/val/test directories")
            return {'valid': False}
        
        # Collect all files by split
        train_files = {}  # {filename: full_path}
        val_files = {}
        test_files = {}
        
        def collect_files(split_dir: Path, file_dict: Dict):
            for class_dir in split_dir.iterdir():
                if class_dir.is_dir():
                    for file in class_dir.glob("*.jpg"):
                        file_dict[file.name] = file
                    for file in class_dir.glob("*.jpeg"):
                        file_dict[file.name] = file
                    for file in class_dir.glob("*.png"):
                        file_dict[file.name] = file
        
        collect_files(train_dir, train_files)
        collect_files(val_dir, val_files)
        collect_files(test_dir, test_files)
        
        if self.verbose:
            print(f"Train: {len(train_files)} files")
            print(f"Val: {len(val_files)} files")
            print(f"Test: {len(test_files)} files")
            print(f"Total: {len(train_files) + len(val_files) + len(test_files)} files")
        
        # Check for overlap (DATA LEAKAGE)
        train_names = set(train_files.keys())
        val_names = set(val_files.keys())
        test_names = set(test_files.keys())
        
        train_val_overlap = train_names & val_names
        train_test_overlap = train_names & test_names
        val_test_overlap = val_names & test_names
        
        has_leakage = False
        
        if train_val_overlap:
            has_leakage = True
            self.errors.append(f"DATA LEAKAGE: {len(train_val_overlap)} files appear in both train and val")
            if self.verbose:
                print(f"\n❌ CRITICAL: {len(train_val_overlap)} files in both TRAIN and VAL")
                if len(train_val_overlap) <= 10:
                    for name in list(train_val_overlap)[:10]:
                        print(f"     - {name}")
        
        if train_test_overlap:
            has_leakage = True
            self.errors.append(f"DATA LEAKAGE: {len(train_test_overlap)} files appear in both train and test")
            if self.verbose:
                print(f"\n❌ CRITICAL: {len(train_test_overlap)} files in both TRAIN and TEST")
                if len(train_test_overlap) <= 10:
                    for name in list(train_test_overlap)[:10]:
                        print(f"     - {name}")
        
        if val_test_overlap:
            has_leakage = True
            self.errors.append(f"DATA LEAKAGE: {len(val_test_overlap)} files appear in both val and test")
            if self.verbose:
                print(f"\n❌ CRITICAL: {len(val_test_overlap)} files in both VAL and TEST")
                if len(val_test_overlap) <= 10:
                    for name in list(val_test_overlap)[:10]:
                        print(f"     - {name}")
        
        if not has_leakage:
            if self.verbose:
                print(f"\n✓ NO DATA LEAKAGE: All splits are disjoint")
            self.info.append("Split integrity verified: No overlap between splits")
        
        # Check for duplicate content (same file copied multiple times)
        if self.verbose:
            print(f"\nChecking for content duplicates...")
        
        all_files = []
        all_files.extend([(f, 'train') for f in train_files.values()])
        all_files.extend([(f, 'val') for f in val_files.values()])
        all_files.extend([(f, 'test') for f in test_files.values()])
        
        # Compute hashes
        file_hashes = defaultdict(list)  # {hash: [(file_path, split), ...]}
        
        for idx, (file_path, split) in enumerate(all_files):
            if self.verbose and (idx + 1) % 100 == 0:
                print(f"  Hashed {idx + 1}/{len(all_files)} files...", end='\r')
            
            try:
                file_hash = self.compute_file_hash(file_path)
                file_hashes[file_hash].append((file_path, split))
            except Exception as e:
                self.warnings.append(f"Could not hash {file_path}: {e}")
        
        if self.verbose:
            print(f"  Hashed {len(all_files)}/{len(all_files)} files... Done!")
        
        # Find content duplicates
        content_duplicates = {h: files for h, files in file_hashes.items() if len(files) > 1}
        
        if content_duplicates:
            self.errors.append(f"CONTENT DUPLICATES: {len(content_duplicates)} unique files duplicated across splits")
            if self.verbose:
                print(f"\n❌ CRITICAL: {len(content_duplicates)} files with duplicate content")
                for idx, (hash_val, files) in enumerate(list(content_duplicates.items())[:5], 1):
                    print(f"\n  Duplicate group {idx}:")
                    for file_path, split in files:
                        print(f"    [{split}] {file_path.name}")
        else:
            if self.verbose:
                print(f"\n✓ NO CONTENT DUPLICATES: All files are unique")
            self.info.append("Content uniqueness verified: No duplicate files")
        
        return {
            'valid': not has_leakage and not content_duplicates,
            'has_leakage': has_leakage,
            'has_content_duplicates': len(content_duplicates) > 0,
            'train_count': len(train_files),
            'val_count': len(val_files),
            'test_count': len(test_files),
            'train_val_overlap': len(train_val_overlap),
            'train_test_overlap': len(train_test_overlap),
            'val_test_overlap': len(val_test_overlap),
            'content_duplicate_groups': len(content_duplicates),
        }
    
    def verify_counts_match(self, source_counts: Dict, split_counts: Dict) -> bool:
        """
        Verify that split counts match source counts
        
        Args:
            source_counts: Dictionary of source class counts
            split_counts: Dictionary with train/val/test counts
            
        Returns:
            True if counts match, False otherwise
        """
        if self.verbose:
            print(f"\n{'='*80}")
            print("VERIFYING COUNT CONSISTENCY")
            print(f"{'='*80}")
        
        source_total = sum(source_counts.values()) if isinstance(source_counts, dict) else source_counts
        split_total = split_counts['train_count'] + split_counts['val_count'] + split_counts['test_count']
        
        if self.verbose:
            print(f"Source images: {source_total}")
            print(f"Split images:  {split_total}")
            print(f"  Train:  {split_counts['train_count']}")
            print(f"  Val:    {split_counts['val_count']}")
            print(f"  Test:   {split_counts['test_count']}")
        
        if source_total != split_total:
            self.errors.append(f"Count mismatch: Source has {source_total} images but split has {split_total}")
            if self.verbose:
                print(f"\n❌ COUNT MISMATCH: {abs(source_total - split_total)} image difference")
            return False
        else:
            if self.verbose:
                print(f"\n✓ COUNTS MATCH: All source images accounted for")
            self.info.append(f"Count consistency verified: {source_total} images")
            return True
    
    def verify_complete(self, source_dir: Path, processed_dir: Path) -> bool:
        """
        Run complete verification suite
        
        Args:
            source_dir: Path to source dataset
            processed_dir: Path to processed split dataset
            
        Returns:
            True if all verifications pass, False otherwise
        """
        if self.verbose:
            print(f"\n{'='*80}")
            print("COMPLETE DATASET VERIFICATION")
            print(f"{'='*80}")
        
        # Clear previous results
        self.errors = []
        self.warnings = []
        self.info = []
        
        # Verify source
        source_result = self.verify_source_dataset(source_dir)
        if not source_result['valid']:
            return False
        
        # Verify split integrity
        split_result = self.verify_split_integrity(processed_dir)
        
        # Verify counts match
        counts_match = self.verify_counts_match(
            source_result['total_images'],
            split_result
        )
        
        # Print summary
        if self.verbose:
            print(f"\n{'='*80}")
            print("VERIFICATION SUMMARY")
            print(f"{'='*80}")
            
            if self.info:
                print(f"\n✓ INFO ({len(self.info)}):")
                for msg in self.info:
                    print(f"  • {msg}")
            
            if self.warnings:
                print(f"\n⚠ WARNINGS ({len(self.warnings)}):")
                for msg in self.warnings:
                    print(f"  • {msg}")
            
            if self.errors:
                print(f"\n❌ ERRORS ({len(self.errors)}):")
                for msg in self.errors:
                    print(f"  • {msg}")
                print(f"\n{'='*80}")
                print("⛔ VERIFICATION FAILED - TRAINING MUST NOT PROCEED")
                print(f"{'='*80}")
            else:
                print(f"\n{'='*80}")
                print("✅ ALL VERIFICATIONS PASSED - SAFE TO TRAIN")
                print(f"{'='*80}")
        
        # Return True only if no errors
        return len(self.errors) == 0
    
    def get_verification_report(self) -> Dict:
        """
        Get verification results as dictionary
        
        Returns:
            Dictionary with all verification results
        """
        return {
            'passed': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
        }


if __name__ == "__main__":
    from config.dataset_config import DATASET_RAW_DIR, DATASET_PROCESSED_DIR
    
    verifier = DatasetVerifier(verbose=True)
    success = verifier.verify_complete(DATASET_RAW_DIR, DATASET_PROCESSED_DIR)
    
    if not success:
        print("\n⛔ Verification failed! Fix issues before training.")
        sys.exit(1)
    else:
        print("\n✅ Verification passed! Dataset is ready for training.")
        sys.exit(0)
