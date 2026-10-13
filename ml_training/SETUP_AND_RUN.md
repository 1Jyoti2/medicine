# Setup and Training Instructions

## Step 1: Install Dependencies

### Create virtual environment (recommended):
```bash
cd ml_training
python -m venv venv
```

### Activate virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- TensorFlow 2.15.0 (~2GB download)
- NumPy, Pillow, scikit-learn
- Matplotlib for plotting
- All other dependencies

**Note:** Installation may take 5-10 minutes depending on internet speed.

---

## Step 2: Verify Installation

```bash
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__); print('GPU:', len(tf.config.list_physical_devices('GPU')) > 0)"
```

Expected output:
```
TensorFlow: 2.15.0
GPU: False  (or True if you have NVIDIA GPU)
```

---

## Step 3: Train the Model

### Quick start (recommended settings):
```bash
python train.py
```

### With custom settings:
```bash
# Example: EfficientNetB0, 20 epochs, smaller batch
python train.py --model EfficientNetB0 --epochs 20 --batch-size 16
```

---

## Step 4: Training Progress

You'll see output like:
```
================================================================================
 LEAF CLASSIFICATION MODEL TRAINING
================================================================================
Start time: 2026-09-17 16:30:00
================================================================================

================================================================================
CREATING DATA GENERATORS
================================================================================
Training samples: 1529
Validation samples: 326
Number of classes: 6
Classes: {'Centella Asiatica': 0, 'Coccinia Grandis': 1, ...}

================================================================================
BUILDING MODEL: MobileNetV2
================================================================================

Model architecture:
  Base model: MobileNetV2
  Input shape: (224, 224, 3)
  Number of classes: 6
  Total parameters: 3,538,984
  Trainable parameters: 525,320

================================================================================
TRAINING MODEL
================================================================================
Phase 1: Training top layers with frozen base
Epochs: 15
Learning rate: 0.001

Epoch 1/15
47/47 [==============================] - 45s 950ms/step - loss: 1.2347 - accuracy: 0.5234 - val_loss: 0.9876 - val_accuracy: 0.6543
Epoch 2/15
47/47 [==============================] - 42s 890ms/step - loss: 0.8765 - accuracy: 0.6789 - val_loss: 0.7654 - val_accuracy: 0.7321
...
```

---

## Step 5: Training Time

### Expected training time:

| Hardware | Phase 1 (15 epochs) | Phase 2 (15 epochs) | Total |
|----------|---------------------|---------------------|-------|
| **CPU only** | 20-30 min | 25-35 min | ~45-65 min |
| **GPU (CUDA)** | 5-8 min | 6-10 min | ~11-18 min |

---

## Step 6: Check Results

After training completes, check:

### 1. Training summary:
```bash
# Find the latest training directory
dir models\training_*

# Read summary
type models\training_YYYYMMDD_HHMMSS\training_summary.txt
```

### 2. View training plots:
Open in image viewer:
```
models\training_YYYYMMDD_HHMMSS\training_history.png
```

### 3. Check test accuracy:
```bash
type models\training_YYYYMMDD_HHMMSS\test_results.json
```

Expected test accuracy: **89-94%** with MobileNetV2

---

## Step 7: Model Files

Your trained model is saved at:
```
models/training_YYYYMMDD_HHMMSS/
├── best_model.keras          ← Use this for deployment
├── model_config.json          ← Configuration for inference
├── training_log.csv           ← Epoch-by-epoch metrics
└── training_history.png       ← Visual performance
```

---

## Troubleshooting

### Issue: "No module named 'tensorflow'"
**Solution:**
```bash
pip install tensorflow==2.15.0
```

### Issue: Out of memory
**Solution:**
```bash
python train.py --batch-size 8
```

### Issue: Training too slow
**Solutions:**
1. Use GPU if available (10x faster)
2. Reduce batch size: `--batch-size 16`
3. Reduce epochs: `--epochs 10 --fine-tune-epochs 10`
4. Use MobileNetV2 instead of EfficientNetB0

### Issue: Low accuracy (<85%)
**Solutions:**
1. Train for more epochs: `--epochs 20 --fine-tune-epochs 20`
2. Try EfficientNetB0: `--model EfficientNetB0`
3. Check `training_history.png` for overfitting
4. Review class distribution (Mikania Micrantha is underrepresented)

---

## GPU Setup (Optional but Recommended)

If you have NVIDIA GPU:

### 1. Install CUDA Toolkit 11.8
Download from: https://developer.nvidia.com/cuda-downloads

### 2. Install cuDNN 8.6
Download from: https://developer.nvidia.com/cudnn

### 3. Verify GPU:
```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

---

## What Happens During Training

### Phase 1: Initial Training (15 epochs)
- Frozen base model (MobileNetV2/EfficientNetB0)
- Only top layers train
- Fast convergence
- Reaches ~85-90% accuracy

### Phase 2: Fine-Tuning (15 epochs)
- Unfreeze last 50% of base layers
- Lower learning rate (10x smaller)
- Fine-tune all layers together
- Reaches ~89-94% accuracy

### Automatic Features:
- ✅ Model checkpoint (saves best model)
- ✅ Early stopping (stops if no improvement)
- ✅ Learning rate reduction (adaptive LR)
- ✅ TensorBoard logging
- ✅ CSV metrics logging

---

## Monitoring with TensorBoard (Optional)

During or after training:
```bash
tensorboard --logdir models/training_YYYYMMDD_HHMMSS/tensorboard
```

Open browser: http://localhost:6006

You'll see:
- Real-time loss curves
- Accuracy curves
- Learning rate schedule
- Model graph

---

## Next Steps After Training

1. ✅ Review training summary and plots
2. ⬜ Test inference on sample images
3. ⬜ Build FastAPI backend (use `best_model.keras`)
4. ⬜ Create inference endpoint
5. ⬜ Update frontend API configuration
6. ⬜ End-to-end testing

---

## Full Training Command Examples

### Fastest (for testing):
```bash
python train.py --epochs 5 --fine-tune-epochs 5 --batch-size 16 --no-fine-tune
```

### Recommended (balanced):
```bash
python train.py
```

### Best accuracy (slower):
```bash
python train.py --model EfficientNetB0 --epochs 20 --fine-tune-epochs 20 --batch-size 8
```

### Production-ready:
```bash
python train.py --model MobileNetV2 --epochs 20 --fine-tune-epochs 15 --batch-size 32
```

---

**Ready? Start training:**
```bash
pip install -r requirements.txt
python train.py
```

Training typically takes **45-65 minutes on CPU** or **10-20 minutes on GPU**.

Your model will be saved and ready for deployment! 🚀
