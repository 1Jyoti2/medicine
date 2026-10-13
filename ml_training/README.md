# ML Training Pipeline - Leaf Classification

Complete machine learning preprocessing pipeline for medicinal leaf classification.

## Project Structure

```
ml_training/
├── config/
│   └── dataset_config.py       # Configuration settings
├── utils/
│   ├── image_validator.py      # Image validation utility
│   ├── duplicate_detector.py   # Duplicate detection
│   ├── dataset_stats.py        # Dataset statistics
│   ├── dataset_splitter.py     # Train/val/test splitting
│   └── data_augmentation.py    # Augmentation configs
├── data/
│   └── leaf_processed/         # Processed dataset (created by pipeline)
│       ├── train/
│       ├── val/
│       └── test/
├── models/                     # Saved models (created during training)
├── reports/                    # Generated reports
├── notebooks/                  # Jupyter notebooks
├── scripts/                    # Training scripts
├── prepare_dataset.py          # Main preprocessing script
└── requirements.txt            # Python dependencies
```

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Dataset Structure

Ensure your raw dataset follows this structure:

```
datasets/Original Image/Leaf_Dataset_Original/
├── Centella Asiatica/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Coccinia Grandis/
│   └── ...
└── [other classes]/
```

## Usage

### Quick Start

Run the complete preprocessing pipeline:

```bash
python prepare_dataset.py
```

This will:
1. ✓ Validate all images (check for corruption, format, size)
2. ✓ Detect duplicate/near-duplicate images
3. ✓ Compute dataset statistics and class distribution
4. ✓ Split dataset into train/val/test (70/15/15)
5. ✓ Generate comprehensive reports

### Command-Line Options

```bash
# Skip validation (if already validated)
python prepare_dataset.py --skip-validation

# Skip duplicate detection
python prepare_dataset.py --skip-duplicate-check

# Resize images during splitting (to 224x224)
python prepare_dataset.py --resize

# Custom source and output directories
python prepare_dataset.py --source /path/to/source --output /path/to/output

# Quiet mode (less verbose)
python prepare_dataset.py --quiet

# View all options
python prepare_dataset.py --help
```

## Output Files

After running the preprocessing pipeline, you'll find:

### Processed Dataset
- `data/leaf_processed/train/` - Training set (70%)
- `data/leaf_processed/val/` - Validation set (15%)
- `data/leaf_processed/test/` - Test set (15%)

### Configuration Files
- `models/leaf_class_mapping.json` - Class name to index mapping
- `data/leaf_processed/split_info.json` - Split statistics

### Reports
- `reports/preprocessing_log.txt` - Complete preprocessing summary
- `reports/dataset_statistics.json` - Detailed dataset statistics
- `reports/corrupted_files.txt` - List of invalid images
- `reports/duplicate_files.txt` - Duplicate image pairs

## Dataset Statistics

The pipeline automatically:
- ✓ Discovers all classes from directory structure
- ✓ Counts images per class
- ✓ Computes class distribution
- ✓ Checks for class imbalance
- ✓ Validates image integrity
- ✓ Detects duplicates using perceptual hashing

## Key Features

### 1. Automatic Class Discovery
No need to manually specify class names - automatically discovered from folder structure.

### 2. Image Validation
- Checks for corrupted files
- Validates formats (JPG, PNG)
- Verifies dimensions and file sizes
- Ensures RGB compatibility

### 3. Duplicate Detection
- Uses perceptual hashing (pHash)
- Detects near-duplicate images
- Configurable similarity threshold

### 4. Stratified Splitting
- Maintains class distribution across splits
- Reproducible with fixed random seed
- No data leakage between splits

### 5. Data Augmentation Ready
- Training augmentation configured (rotation, flip, zoom, etc.)
- Validation/test: only rescaling (no augmentation)
- Prevents data leakage

## Configuration

Edit `config/dataset_config.py` to customize:

```python
# Image size
IMAGE_SIZE = (224, 224)

# Split ratios
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Random seed
RANDOM_SEED = 42

# Augmentation parameters
TRAIN_AUGMENTATION = {
    'rotation_range': 20,
    'zoom_range': 0.2,
    'horizontal_flip': True,
    # ...
}
```

## Next Steps

After preprocessing:

1. **Review Reports**: Check `reports/` directory for any issues
2. **Train Model**: Use the processed dataset in `data/leaf_processed/`
3. **Use Class Mapping**: Load `models/leaf_class_mapping.json` for predictions

## Troubleshooting

### Issue: "No valid images found"
- Check that dataset path is correct
- Verify images are in supported formats (JPG, PNG)
- Review `reports/corrupted_files.txt` for issues

### Issue: "Class imbalance warning"
- Normal for some datasets
- Consider data augmentation for underrepresented classes
- Use class weights during training

### Issue: "Import errors"
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment if using one

## Technical Details

### Image Validation
- Minimum size: 50x50 pixels
- Maximum size: 10000x10000 pixels
- Minimum file size: 1 KB
- Maximum file size: 50 MB

### Duplicate Detection
- Algorithm: Perceptual hashing (difference hash)
- Hash size: 16
- Hamming distance threshold: 5

### Data Augmentation
- Rotation: ±20 degrees
- Width/Height shift: 20%
- Shear: 20%
- Zoom: ±20%
- Flips: Horizontal and vertical
- Brightness: ±20%

## License

This preprocessing pipeline is part of the MediLeaf project.

## Contact

For issues or questions, please refer to the main project documentation.
