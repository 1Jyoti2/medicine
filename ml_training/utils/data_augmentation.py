"""
Data Augmentation Utility
Defines augmentation pipelines for training, validation, and test sets
"""
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from typing import Tuple

from config.dataset_config import (
    TRAIN_AUGMENTATION,
    VAL_TEST_PREPROCESSING,
    IMAGE_SIZE,
    BATCH_SIZE,
)


class DataAugmentation:
    """
    Manages data augmentation for different dataset splits
    """
    
    def __init__(self, image_size: Tuple[int, int] = IMAGE_SIZE, 
                 batch_size: int = BATCH_SIZE):
        """
        Initialize data augmentation
        
        Args:
            image_size: Target image size (height, width)
            batch_size: Batch size for data generators
        """
        self.image_size = image_size
        self.batch_size = batch_size
        
        # Training augmentation (aggressive)
        self.train_datagen = self._create_train_datagen()
        
        # Validation and test preprocessing (no augmentation)
        self.val_datagen = self._create_val_test_datagen()
        self.test_datagen = self._create_val_test_datagen()
    
    def _create_train_datagen(self) -> ImageDataGenerator:
        """
        Create training data generator with augmentation
        
        Returns:
            ImageDataGenerator for training
        """
        return ImageDataGenerator(
            rescale=1./255,  # Normalize to [0, 1]
            rotation_range=TRAIN_AUGMENTATION['rotation_range'],
            width_shift_range=TRAIN_AUGMENTATION['width_shift_range'],
            height_shift_range=TRAIN_AUGMENTATION['height_shift_range'],
            shear_range=TRAIN_AUGMENTATION['shear_range'],
            zoom_range=TRAIN_AUGMENTATION['zoom_range'],
            horizontal_flip=TRAIN_AUGMENTATION['horizontal_flip'],
            vertical_flip=TRAIN_AUGMENTATION['vertical_flip'],
            fill_mode=TRAIN_AUGMENTATION['fill_mode'],
            brightness_range=TRAIN_AUGMENTATION.get('brightness_range'),
        )
    
    def _create_val_test_datagen(self) -> ImageDataGenerator:
        """
        Create validation/test data generator (no augmentation)
        
        Returns:
            ImageDataGenerator for validation/test
        """
        return ImageDataGenerator(
            rescale=VAL_TEST_PREPROCESSING['rescale']
        )
    
    def get_train_generator(self, train_dir, class_mode='categorical', 
                           shuffle=True, seed=None):
        """
        Get training data generator
        
        Args:
            train_dir: Path to training directory
            class_mode: Type of label arrays (categorical, binary, etc.)
            shuffle: Whether to shuffle data
            seed: Random seed for reproducibility
            
        Returns:
            Training data generator
        """
        return self.train_datagen.flow_from_directory(
            train_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode=class_mode,
            shuffle=shuffle,
            seed=seed
        )
    
    def get_val_generator(self, val_dir, class_mode='categorical', 
                         shuffle=False, seed=None):
        """
        Get validation data generator
        
        Args:
            val_dir: Path to validation directory
            class_mode: Type of label arrays
            shuffle: Whether to shuffle data
            seed: Random seed
            
        Returns:
            Validation data generator
        """
        return self.val_datagen.flow_from_directory(
            val_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode=class_mode,
            shuffle=shuffle,
            seed=seed
        )
    
    def get_test_generator(self, test_dir, class_mode='categorical', 
                          shuffle=False, seed=None):
        """
        Get test data generator
        
        Args:
            test_dir: Path to test directory
            class_mode: Type of label arrays
            shuffle: Whether to shuffle data
            seed: Random seed
            
        Returns:
            Test data generator
        """
        return self.test_datagen.flow_from_directory(
            test_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode=class_mode,
            shuffle=shuffle,
            seed=seed
        )
    
    def get_config_summary(self) -> dict:
        """
        Get augmentation configuration summary
        
        Returns:
            Dictionary with configuration details
        """
        return {
            'image_size': self.image_size,
            'batch_size': self.batch_size,
            'train_augmentation': TRAIN_AUGMENTATION,
            'val_test_preprocessing': VAL_TEST_PREPROCESSING,
        }
    
    @staticmethod
    def preprocess_single_image(image_array: np.ndarray, 
                               target_size: Tuple[int, int] = IMAGE_SIZE) -> np.ndarray:
        """
        Preprocess a single image for inference
        
        Args:
            image_array: Image as numpy array
            target_size: Target size for resizing
            
        Returns:
            Preprocessed image array
        """
        from PIL import Image
        
        # Convert to PIL Image
        if image_array.dtype != np.uint8:
            image_array = (image_array * 255).astype(np.uint8)
        
        img = Image.fromarray(image_array)
        
        # Resize
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to array and normalize
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array


if __name__ == "__main__":
    # Test augmentation setup
    aug = DataAugmentation()
    config = aug.get_config_summary()
    
    print("Data Augmentation Configuration:")
    print("=" * 80)
    print(f"Image size: {config['image_size']}")
    print(f"Batch size: {config['batch_size']}")
    print("\nTraining augmentation:")
    for key, value in config['train_augmentation'].items():
        print(f"  {key}: {value}")
    print("\nValidation/Test preprocessing:")
    for key, value in config['val_test_preprocessing'].items():
        print(f"  {key}: {value}")
