"""
Duplicate Image Detection Utility
Uses perceptual hashing to detect duplicate and near-duplicate images
"""
import os
from pathlib import Path
from typing import List, Tuple, Dict, Set
from PIL import Image
import numpy as np
from collections import defaultdict
import hashlib

from config.dataset_config import DUPLICATE_HASH_SIZE, DUPLICATE_THRESHOLD


class DuplicateDetector:
    """
    Detects duplicate and near-duplicate images using perceptual hashing
    """
    
    def __init__(self, hash_size: int = DUPLICATE_HASH_SIZE, 
                 threshold: int = DUPLICATE_THRESHOLD, verbose: bool = True):
        """
        Initialize duplicate detector
        
        Args:
            hash_size: Size of perceptual hash (larger = more precise)
            threshold: Hamming distance threshold for duplicates (0 = exact match)
            verbose: Print detection progress
        """
        self.hash_size = hash_size
        self.threshold = threshold
        self.verbose = verbose
        self.image_hashes = {}  # {file_path: hash}
        self.duplicates = []    # [(file1, file2, distance), ...]
    
    def compute_phash(self, image_path: Path) -> str:
        """
        Compute perceptual hash (pHash) for an image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Hexadecimal hash string
        """
        try:
            with Image.open(image_path) as img:
                # Convert to grayscale
                img = img.convert('L')
                
                # Resize to hash_size + 1 (for DCT)
                img = img.resize((self.hash_size + 1, self.hash_size), Image.Resampling.LANCZOS)
                
                # Convert to numpy array
                pixels = np.array(img, dtype=np.float32)
                
                # Compute DCT (Discrete Cosine Transform) approximation
                # Using difference hash as fallback (simpler but effective)
                dct = self._simple_dct(pixels)
                
                # Keep only top-left hash_size x hash_size
                dct_low = dct[:self.hash_size, :self.hash_size]
                
                # Compute median
                median = np.median(dct_low)
                
                # Generate hash: 1 if > median, 0 otherwise
                hash_bits = dct_low > median
                
                # Convert to hex string
                hash_array = hash_bits.flatten()
                hash_hex = self._bits_to_hex(hash_array)
                
                return hash_hex
        
        except Exception as e:
            if self.verbose:
                print(f"Warning: Could not compute hash for {image_path}: {e}")
            return None
    
    def _simple_dct(self, pixels: np.ndarray) -> np.ndarray:
        """
        Simple DCT approximation using difference method
        (Faster than full DCT, good enough for duplicate detection)
        
        Args:
            pixels: Image pixel array
            
        Returns:
            DCT-like array
        """
        # Compute horizontal differences
        diff = np.diff(pixels, axis=1)
        return diff
    
    def _bits_to_hex(self, bits: np.ndarray) -> str:
        """
        Convert bit array to hexadecimal string
        
        Args:
            bits: Boolean array
            
        Returns:
            Hexadecimal string
        """
        # Convert bool to int and then to hex
        hex_str = ''
        for i in range(0, len(bits), 4):
            chunk = bits[i:i+4]
            val = 0
            for bit in chunk:
                val = (val << 1) | int(bit)
            hex_str += format(val, 'x')
        return hex_str
    
    def _hamming_distance(self, hash1: str, hash2: str) -> int:
        """
        Compute Hamming distance between two hashes
        
        Args:
            hash1: First hash string
            hash2: Second hash string
            
        Returns:
            Hamming distance (number of differing bits)
        """
        if hash1 is None or hash2 is None:
            return float('inf')
        
        if len(hash1) != len(hash2):
            return float('inf')
        
        distance = 0
        for c1, c2 in zip(hash1, hash2):
            # Convert hex chars to int and XOR
            xor = int(c1, 16) ^ int(c2, 16)
            # Count set bits
            distance += bin(xor).count('1')
        
        return distance
    
    def detect_duplicates(self, image_files: List[Path]) -> Dict:
        """
        Detect duplicate images in a list of files
        
        Args:
            image_files: List of image file paths
            
        Returns:
            Dictionary with duplicate detection results
        """
        if self.verbose:
            print(f"\n{'='*80}")
            print("DUPLICATE DETECTION")
            print(f"{'='*80}")
            print(f"Computing hashes for {len(image_files)} images...")
        
        # Reset
        self.image_hashes = {}
        self.duplicates = []
        
        # Compute hashes for all images
        for idx, image_path in enumerate(image_files, 1):
            hash_val = self.compute_phash(image_path)
            if hash_val is not None:
                self.image_hashes[str(image_path)] = hash_val
            
            if self.verbose and idx % 100 == 0:
                print(f"Computed {idx}/{len(image_files)} hashes...", end='\r')
        
        if self.verbose:
            print(f"Computed {len(self.image_hashes)}/{len(image_files)} hashes... Done!")
            print(f"\nComparing hashes to find duplicates (threshold={self.threshold})...")
        
        # Find duplicates by comparing all pairs
        file_paths = list(self.image_hashes.keys())
        total_comparisons = len(file_paths) * (len(file_paths) - 1) // 2
        comparisons_done = 0
        
        for i in range(len(file_paths)):
            for j in range(i + 1, len(file_paths)):
                hash1 = self.image_hashes[file_paths[i]]
                hash2 = self.image_hashes[file_paths[j]]
                
                distance = self._hamming_distance(hash1, hash2)
                
                if distance <= self.threshold:
                    self.duplicates.append((
                        file_paths[i],
                        file_paths[j],
                        distance
                    ))
                
                comparisons_done += 1
                if self.verbose and comparisons_done % 10000 == 0:
                    print(f"Compared {comparisons_done}/{total_comparisons} pairs...", end='\r')
        
        if self.verbose:
            print(f"Compared {total_comparisons}/{total_comparisons} pairs... Done!")
            self._print_summary()
        
        return self.get_summary()
    
    def detect_duplicates_in_dataset(self, dataset_path: Path) -> Dict:
        """
        Detect duplicates in entire dataset directory
        
        Args:
            dataset_path: Path to dataset directory with class subdirectories
            
        Returns:
            Dictionary with duplicate detection results
        """
        # Collect all image files
        image_files = []
        for class_dir in dataset_path.iterdir():
            if class_dir.is_dir():
                for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                    image_files.extend(class_dir.glob(f"*{ext}"))
        
        return self.detect_duplicates(image_files)
    
    def _print_summary(self):
        """Print duplicate detection summary"""
        print(f"\n{'='*80}")
        print("DUPLICATE DETECTION SUMMARY")
        print(f"{'='*80}")
        
        print(f"Total images processed:  {len(self.image_hashes)}")
        print(f"Duplicate pairs found:   {len(self.duplicates)}")
        
        if len(self.duplicates) > 0:
            print(f"\nDuplicate breakdown by Hamming distance:")
            distance_counts = defaultdict(int)
            for _, _, distance in self.duplicates:
                distance_counts[distance] += 1
            
            for distance in sorted(distance_counts.keys()):
                print(f"  Distance {distance:2d}: {distance_counts[distance]:4d} pairs")
            
            # Show some examples
            print(f"\nFirst 5 duplicate pairs:")
            for i, (file1, file2, distance) in enumerate(self.duplicates[:5], 1):
                print(f"\n  {i}. Hamming distance: {distance}")
                print(f"     File 1: {Path(file1).name}")
                print(f"     File 2: {Path(file2).name}")
    
    def get_summary(self) -> Dict:
        """
        Get duplicate detection summary as dictionary
        
        Returns:
            Dictionary with detection statistics
        """
        return {
            'total_images': len(self.image_hashes),
            'duplicate_pairs': len(self.duplicates),
            'duplicate_files': self._get_duplicate_files(),
            'unique_images': len(self.image_hashes) - len(self._get_duplicate_files()),
        }
    
    def _get_duplicate_files(self) -> Set[str]:
        """
        Get set of all files involved in duplicates
        
        Returns:
            Set of file paths
        """
        duplicate_files = set()
        for file1, file2, _ in self.duplicates:
            duplicate_files.add(file1)
            duplicate_files.add(file2)
        return duplicate_files
    
    def get_files_to_remove(self) -> List[str]:
        """
        Get list of duplicate files to remove (keeps one from each group)
        
        Returns:
            List of file paths to remove
        """
        # Build groups of duplicates
        from collections import defaultdict
        groups = defaultdict(set)
        
        for file1, file2, distance in self.duplicates:
            # Find existing group
            group_id = None
            for gid, members in groups.items():
                if file1 in members or file2 in members:
                    group_id = gid
                    break
            
            if group_id is None:
                # Create new group
                group_id = len(groups)
            
            groups[group_id].add(file1)
            groups[group_id].add(file2)
        
        # From each group, keep the first file and remove others
        files_to_remove = []
        for group_members in groups.values():
            sorted_members = sorted(group_members)
            files_to_remove.extend(sorted_members[1:])  # Keep first, remove rest
        
        return files_to_remove
    
    def save_duplicate_report(self, output_path: Path):
        """
        Save duplicate detection report to file
        
        Args:
            output_path: Path to output file
        """
        if len(self.duplicates) == 0:
            if self.verbose:
                print("\nNo duplicates found!")
            return
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("DUPLICATE IMAGES REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total images processed: {len(self.image_hashes)}\n")
            f.write(f"Duplicate pairs found: {len(self.duplicates)}\n")
            f.write(f"Files involved in duplicates: {len(self._get_duplicate_files())}\n\n")
            
            f.write("\nDUPLICATE PAIRS\n")
            f.write("-" * 80 + "\n\n")
            
            for idx, (file1, file2, distance) in enumerate(self.duplicates, 1):
                f.write(f"{idx}. Hamming distance: {distance}\n")
                f.write(f"   File 1: {file1}\n")
                f.write(f"   File 2: {file2}\n\n")
            
            # Files to remove
            files_to_remove = self.get_files_to_remove()
            f.write(f"\n{'='*80}\n")
            f.write(f"RECOMMENDED FILES TO REMOVE ({len(files_to_remove)} files)\n")
            f.write(f"{'='*80}\n\n")
            
            for file_path in files_to_remove:
                f.write(f"  {file_path}\n")
        
        if self.verbose:
            print(f"\nDuplicate report saved to: {output_path}")


if __name__ == "__main__":
    # Test duplicate detection
    from config.dataset_config import DATASET_RAW_DIR, DUPLICATE_FILES_LOG
    
    detector = DuplicateDetector(verbose=True)
    results = detector.detect_duplicates_in_dataset(DATASET_RAW_DIR)
    
    # Save report
    detector.save_duplicate_report(DUPLICATE_FILES_LOG)
    
    print("\nDuplicate detection complete!")
