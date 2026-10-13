"""
Dataset Configuration for Leaf Classification
Defines all preprocessing parameters, paths, and constants
"""
import os
from pathlib import Path

# ============================================================================
# PATHS
# ============================================================================
BASE_DIR = Path(__file__).parent.parent.parent
DATASET_RAW_DIR = BASE_DIR / "datasets" / "Original Image" / "Leaf_Dataset_Original"
DATASET_PROCESSED_DIR = BASE_DIR / "ml_training" / "data" / "leaf_processed"
MODELS_DIR = BASE_DIR / "ml_training" / "models"
REPORTS_DIR = BASE_DIR / "ml_training" / "reports"

# ============================================================================
# DATASET PARAMETERS
# ============================================================================
# Image preprocessing
IMAGE_SIZE = (224, 224)  # Standard for transfer learning models
TARGET_CHANNELS = 3  # RGB
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png']

# Dataset splits (must sum to 1.0)
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Random seed for reproducibility
RANDOM_SEED = 42

# ============================================================================
# DATA AUGMENTATION - TRAINING ONLY
# ============================================================================
TRAIN_AUGMENTATION = {
    'rotation_range': 20,           # Degrees
    'width_shift_range': 0.2,       # Fraction of total width
    'height_shift_range': 0.2,      # Fraction of total height
    'shear_range': 0.2,             # Shear intensity
    'zoom_range': 0.2,              # [0.8, 1.2]
    'horizontal_flip': True,
    'vertical_flip': True,
    'fill_mode': 'nearest',
    'brightness_range': [0.8, 1.2], # Brightness variation
}

# Validation and Test: Only rescaling (no augmentation)
VAL_TEST_PREPROCESSING = {
    'rescale': 1./255,  # Normalize to [0, 1]
}

# ============================================================================
# VALIDATION PARAMETERS
# ============================================================================
MIN_IMAGE_SIZE = (50, 50)      # Minimum valid image dimensions
MAX_IMAGE_SIZE = (10000, 10000) # Maximum valid image dimensions
MIN_FILE_SIZE = 1024            # 1 KB minimum file size
MAX_FILE_SIZE = 50 * 1024 * 1024 # 50 MB maximum file size

# ============================================================================
# DUPLICATE DETECTION
# ============================================================================
DUPLICATE_HASH_SIZE = 16        # Hash size for perceptual hashing
DUPLICATE_THRESHOLD = 5         # Hamming distance threshold (lower = more strict)

# ============================================================================
# CLASS BALANCING
# ============================================================================
MIN_SAMPLES_PER_CLASS = 50      # Minimum images required per class
CLASS_IMBALANCE_THRESHOLD = 0.3 # Warn if class has < 30% of average

# ============================================================================
# OUTPUT FILES
# ============================================================================
CLASS_MAPPING_FILE = MODELS_DIR / "leaf_class_mapping.json"
DATASET_STATS_FILE = REPORTS_DIR / "dataset_statistics.json"
CORRUPTED_FILES_LOG = REPORTS_DIR / "corrupted_files.txt"
DUPLICATE_FILES_LOG = REPORTS_DIR / "duplicate_files.txt"
PREPROCESSING_LOG = REPORTS_DIR / "preprocessing_log.txt"

# ============================================================================
# TRAINING PARAMETERS
# ============================================================================
BATCH_SIZE = 32
EPOCHS = 15  # Initial training epochs
FINE_TUNE_EPOCHS = 15  # Fine-tuning epochs
LEARNING_RATE = 0.001
FINE_TUNE_LEARNING_RATE = 0.0001
PATIENCE_EARLY_STOPPING = 10
PATIENCE_REDUCE_LR = 5

# ============================================================================
# MODEL PARAMETERS
# ============================================================================
MODEL_ARCHITECTURE = 'EfficientNetB3'  # Options: EfficientNetB3, MobileNetV2, ResNet50
PRETRAINED_WEIGHTS = 'imagenet'
INCLUDE_TOP = False
POOLING = 'avg'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def ensure_directories():
    """Create necessary directories if they don't exist"""
    dirs = [
        DATASET_PROCESSED_DIR / "train",
        DATASET_PROCESSED_DIR / "val",
        DATASET_PROCESSED_DIR / "test",
        MODELS_DIR,
        REPORTS_DIR,
    ]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

def get_config_summary():
    """Return configuration summary as dictionary"""
    return {
        'dataset_source': str(DATASET_RAW_DIR),
        'dataset_processed': str(DATASET_PROCESSED_DIR),
        'image_size': IMAGE_SIZE,
        'split_ratios': {
            'train': TRAIN_RATIO,
            'val': VAL_RATIO,
            'test': TEST_RATIO
        },
        'random_seed': RANDOM_SEED,
        'augmentation': TRAIN_AUGMENTATION,
        'supported_formats': SUPPORTED_FORMATS,
    }

if __name__ == "__main__":
    # Print configuration when run directly
    import json
    print("Dataset Configuration Summary")
    print("=" * 80)
    config = get_config_summary()
    print(json.dumps(config, indent=2))
