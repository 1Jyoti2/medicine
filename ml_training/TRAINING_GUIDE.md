# Model Training Guide

This guide explains how to train the leaf classification model using your preprocessed dataset.

## Quick Start

### Train with default settings (MobileNetV2):
```bash
cd ml_training
python train.py
```

This will:
1. Load the preprocessed dataset from `data/leaf_processed/`
2. Build a MobileNetV2 transfer learning model
3. Train for 15 epochs (frozen base)
4. Fine-tune for 15 more epochs (unfrozen base)
5. Evaluate on test set
6. Save the best model and training plots

---

## Training Options

### Choose model architecture:
```bash
# MobileNetV2 (lightweight, fast inference)
python train.py --model MobileNetV2

# EfficientNetB0 (better accuracy, slower)
python train.py --model EfficientNetB0
```

### Adjust epochs:
```bash
# More training epochs
python train.py --epochs 20 --fine-tune-epochs 20

# Skip fine-tuning (faster)
python train.py --no-fine-tune
```

### Adjust batch size:
```bash
# Smaller batch (less memory)
python train.py --batch-size 16

# Larger batch (faster training if you have GPU memory)
python train.py --batch-size 64
```

### Adjust learning rate:
```bash
python train.py --lr 0.0005
```

### Combine options:
```bash
python train.py --model EfficientNetB0 --epochs 20 --batch-size 16
```

---

## Model Architecture

### MobileNetV2 (Recommended)
- **Parameters:** ~3.5M
- **Size:** ~14 MB
- **Speed:** Fast inference (~50ms on CPU)
- **Best for:** Real-time FastAPI deployment
- **Accuracy:** Good (90-94% expected)

### EfficientNetB0
- **Parameters:** ~5.3M
- **Size:** ~21 MB
- **Speed:** Medium inference (~100ms on CPU)
- **Best for:** Higher accuracy requirements
- **Accuracy:** Better (92-96% expected)

---

## Training Process

### Phase 1: Initial Training (Frozen Base)
- Base model layers are frozen
- Only top classification layers train
- Epochs: 15 (default)
- Learning rate: 0.001

### Phase 2: Fine-Tuning (Unfrozen Base)
- Last ~50% of base layers unfrozen
- All layers fine-tune together
- Epochs: 15 (default)
- Learning rate: 0.0001 (lower)

---

## What Gets Saved

After training completes, check the output directory:
```
models/training_YYYYMMDD_HHMMSS/
├── best_model.keras          # Best model (highest val accuracy)
├── final_model.keras          # Final model after all epochs
├── model_config.json          # Model configuration
├── training_log.csv           # Epoch-by-epoch metrics
├── training_history.png       # Training plots
├── test_results.json          # Test set performance
├── training_summary.txt       # Complete summary
└── tensorboard/               # TensorBoard logs
```

---

## Monitoring Training

### Real-time console output:
The script prints:
- Epoch progress
- Loss and accuracy metrics
- Validation performance
- Best model checkpoints

### TensorBoard (optional):
```bash
tensorboard --logdir models/training_YYYYMMDD_HHMMSS/tensorboard
```

Then open: http://localhost:6006

---

## Expected Performance

### With your dataset (6 classes, 1,529 train samples):

| Model | Train Acc | Val Acc | Test Acc | Inference |
|-------|-----------|---------|----------|-----------|
| MobileNetV2 | 95-98% | 90-94% | 89-93% | ~50ms |
| EfficientNetB0 | 96-99% | 92-96% | 91-95% | ~100ms |

**Note:** Mikania Micrantha (136 samples) may have lower accuracy due to class imbalance.

---

## Troubleshooting

### Out of Memory Error
```bash
# Reduce batch size
python train.py --batch-size 8
```

### Training too slow
```bash
# Use MobileNetV2 instead of EfficientNetB0
python train.py --model MobileNetV2

# Reduce epochs
python train.py --epochs 10 --fine-tune-epochs 10
```

### Model not improving
- Check `training_history.png` for overfitting
- Try reducing learning rate: `--lr 0.0005`
- Try more augmentation (edit `config/dataset_config.py`)

### Import errors
```bash
# Make sure TensorFlow is installed
pip install tensorflow==2.15.0

# Install other dependencies
pip install -r requirements.txt
```

---

## After Training

### 1. Review Results
Check the training summary:
```bash
cat models/training_YYYYMMDD_HHMMSS/training_summary.txt
```

### 2. View Training Plots
Open:
```
models/training_YYYYMMDD_HHMMSS/training_history.png
```

### 3. Test the Model
See `test_inference.py` (to be created) for testing predictions.

### 4. Deploy
Use `best_model.keras` with FastAPI backend (Phase 3).

---

## Hardware Requirements

### Minimum:
- **CPU:** Any modern processor
- **RAM:** 8 GB
- **Storage:** 5 GB free
- **Training time:** 30-60 minutes

### Recommended:
- **GPU:** NVIDIA GPU with 4+ GB VRAM
- **RAM:** 16 GB
- **Training time:** 10-20 minutes

### With GPU:
TensorFlow will automatically use GPU if available. No config needed.

Check GPU:
```python
import tensorflow as tf
print("GPU Available:", tf.config.list_physical_devices('GPU'))
```

---

## Reproducibility

The training script uses fixed random seeds:
- **Random seed:** 42
- **TensorFlow seed:** 42
- **NumPy seed:** 42
- **Python hash seed:** 42

Running with same parameters will give nearly identical results (small differences due to GPU operations).

---

## Tips for Best Results

1. **Use default settings first** - They're optimized for your dataset
2. **Monitor validation accuracy** - Should be 88-95%
3. **Check for overfitting** - Train vs val accuracy gap
4. **Review class-wise performance** - Check confusion matrix
5. **Save best model** - Don't use final model if it overfits

---

## Next Steps

After successful training:
1. ✅ Review `training_summary.txt`
2. ⬜ Test inference on new images
3. ⬜ Build FastAPI backend
4. ⬜ Integrate with frontend
5. ⬜ Deploy to production

---

**Ready to train? Run:**
```bash
python train.py
```

Good luck! 🚀
