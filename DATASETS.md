# Dataset Information & Storage Requirements

Medicine AI incorporates three distinct machine learning modalities:
1. **Medicinal Leaf Identification (CNN Transfer Learning)**
2. **Clinical Prescription OCR (EasyOCR + Rule-based NER)**
3. **Pharmaceutical Pill Identification (MobileNetV2 + Visual Embeddings)**

To prevent repository bloat and ensure fast cloning, raw bulk image datasets (~3 GB) are maintained separately from the Git repository. The repository includes all metadata mappings, split manifests, trained model checkpoints, and training scripts.

---

## 1. Dataset Breakdown

| Dataset | Disk Size | Count / Classes | Format & Resolution | Storage Location |
|---|---|---|---|---|
| **Medicinal Leaf Dataset** | ~1.49 GB | 1,279 images across 6 classes (*Centella Asiatica*, *Coccinia Grandis*, *Eclipta Prostrata*, *Mikania Micrantha*, *Murraya koenigii*, *Stephania Japonica*) | JPG / PNG ($224 \times 224$) | `ml_training/data/leaf_processed/` or `datasets/Original Image/` |
| **Handwritten Prescription Scans** | ~25 MB | 30 real-world doctor prescriptions | High-res JPG ($1200 \times 1800$) | `datasets/handwritten_pages_jpg/` |
| **Pharmaceutical Pill Benchmark** | ~50 MB | 20 reference pill formulations (NIH / ePillID benchmark) | RGB JPG ($224 \times 224$) | `datasets/small_dataset_20_images/` & `pill_training/data/processed/` |

---

## 2. Directory Structure

When downloading or preparing datasets locally for retraining, organize files as follows:

```
Medicine/
├── datasets/
│   ├── Original Image/
│   │   └── Leaf_Dataset_Original/
│   │       ├── Centella Asiatica/
│   │       ├── Coccinia Grandis/
│   │       ├── Eclipta Prostrata/
│   │       ├── Mikania Micrantha/
│   │       ├── Murraya koenigii/
│   │       └── Stephania Japonica/
│   ├── handwritten_pages_jpg/
│   │   ├── prescription_001.jpg
│   │   └── ...
│   └── small_dataset_20_images/
│       └── small_dataset/
│           └── ePillID_data/
└── ml_training/
    └── data/
        ├── leaf_processed/
        │   ├── train/
        │   ├── val/
        │   └── test/
        ├── frontend_plants_data.js       <-- Included in Git
        └── medicinal_plants_metadata.json <-- Included in Git
```

---

## 3. Pretrained Weights (Git LFS)

You do **not** need to download the full 3 GB dataset to run the application or serve predictions.
The trained PyTorch checkpoints are versioned in this repository using Git LFS:
- **Medicinal Leaf Classifier:** `ml_training/models/training_20260919_135002/final_model.pth`
- **Pill Identifier:** `pill_training/models/pill_training_20260921_125546/final_model.pth`

To pull model weights when cloning:
```bash
git lfs install
git lfs pull
```

---

## 4. Retraining Pipeline

If you wish to retrain or fine-tune models from scratch:

1. **Leaf Classifier:**
   ```bash
   python ml_training/prepare_dataset.py
   python ml_training/train.py
   python ml_training/evaluate.py
   ```

2. **Pill Classifier:**
   ```bash
   python pill_training/prepare_dataset.py
   python pill_training/train.py
   ```
