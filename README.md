# Medicine AI — Full-Stack Intelligent Healthcare & Pharmacology Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14.0%2Bcpu-EE4C2C?style=flat&logo=pytorch)](https://pytorch.org)
[![React](https://img.shields.io/badge/React-19.2.8-61DAFB?style=flat&logo=react)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-8.2.2-646CFF?style=flat&logo=vite)](https://vite.dev)
[![EasyOCR](https://img.shields.io/badge/EasyOCR-1.7.2-4B8BBE?style=flat)](https://github.com/JaidedAI/EasyOCR)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.3.3-38B2AC?style=flat&logo=tailwindcss)](https://tailwindcss.com)

A comprehensive, production-ready healthcare intelligence system combining deep learning, optical character recognition (OCR), and visual pharmacology. The application delivers real-time AI inference across three clinical and botanical domains without reliance on mock data or simulated responses.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Main Features](#2-main-features)
3. [Technology Stack](#3-technology-stack)
4. [Project Structure](#4-project-structure)
5. [ML Models](#5-ml-models)
6. [Dataset Information](#6-dataset-information)
7. [Training Process](#7-training-process)
8. [Model Evaluation](#8-model-evaluation)
9. [FastAPI Backend](#9-fastapi-backend)
10. [API Endpoints](#10-api-endpoints)
11. [Frontend Setup](#11-frontend-setup)
12. [Backend Setup](#12-backend-setup)
13. [Environment Variables](#13-environment-variables)
14. [How to Run the Project](#14-how-to-run-the-project)
15. [How to Test the APIs](#15-how-to-test-the-apis)
16. [How to Train Models](#16-how-to-train-models)
17. [Where Trained Checkpoints are Stored](#17-where-trained-checkpoints-are-stored)
18. [Troubleshooting](#18-troubleshooting)
19. [Known Limitations](#19-known-limitations)

---

## 1. Project Overview

Medicine AI addresses critical challenges in modern healthcare, pharmacognosy, and prescription management by providing three specialized machine learning services in a single unified platform:

1. **Medicinal Leaf Identification:** Recognizes medicinal plants from leaf photographs, retrieves botanical classifications, and outlines phytochemicals, therapeutic uses, and contraindications.
2. **Clinical Prescription OCR:** Transcribes complex handwritten doctor prescriptions, extracts patient and physician metadata, and parses prescribed medications into structured dosage regimens.
3. **Pharmaceutical Pill Identification:** Identifies commercial tablets and capsules from images, verifying drug names, strengths, manufacturers, and National Drug Code (NDC) references.

---

## 2. Main Features

- **Real-Time PyTorch Inference:** Pre-warmed CNN models delivering leaf predictions in ~108 ms and pill predictions in ~52 ms.
- **Full Prescription Digitization:** EasyOCR-powered line clustering and regex clinical entity parser extracting medication names, dosages, frequencies, and durations.
- **Detailed Pharmacognosy Profiles:** Curated botanical metadata database covering active compounds (e.g. *Asiaticoside*, *Wedelolactone*, *Mahanimbine*), preparation methods, and precautions.
- **Clinical History Tracking:** In-memory session tracking recording diagnostic scans with confidence scores, timestamps, and full report lookups.
- **PDF Report Generation:** Client-side prescription report export via `jspdf`.
- **Zero Disk Residue & Memory Safety:** Uploads are processed in-memory via chunked `io.BytesIO` streams with decompression bomb protection (`MAX_IMAGE_PIXELS = 50,000,000`).
- **Path Traversal & MIME Validation:** Magic-byte inspection (`\xff\xd8\xff`, `\x89PNG`, etc.), strict extension whitelisting, and regex filename sanitization.

---

## 3. Technology Stack

### Runtime & Production Requirements
- **Backend Framework:** FastAPI (v0.115.12) on Uvicorn ASGI server
- **Deep Learning Runtime:** PyTorch (v2.14.0+cpu), Torchvision (v0.29.0+cpu)
- **Computer Vision & OCR:** OpenCV (Headless), Pillow (PIL), EasyOCR (v1.7.2), NumPy (v2.5.2)
- **Frontend Stack:** React 19, Vite 8, TailwindCSS v4, React Router DOM 7, Lucide React, Axios, jsPDF
- **Runtime Environment:** Python 3.10+ and Node.js 18+

### Development & Training Requirements
- **Training Libraries:** `scikit-learn>=1.4.0`, `matplotlib>=3.8.0`, `tqdm>=4.66.0`
- **Testing & Benchmarking:** `requests>=2.31.0`, `pytest>=8.0.0`, `httpx>=0.27.0`
- **Frontend Linter:** `oxlint>=1.79.0`

---

## 4. Project Structure

```
Medicine/
├── backend/                              # Production FastAPI Backend
│   ├── main.py                           # API router, lifespan management, & exception guards
│   └── security.py                       # Magic bytes, stream limiters, & path sanitization
├── ml_training/                          # Leaf Classification Model Subsystem
│   ├── inference/                        # LeafClassifier inference service
│   │   ├── predictor.py                  # PyTorch LeafClassifier service
│   │   └── preprocessing.py              # Single-pass RGB preprocessor
│   ├── models/                           # Trained leaf model checkpoints
│   │   └── training_20260919_135002/     # Active production model artifact directory
│   │       ├── final_model.pth           # Trained PyTorch weights (10.6 MB)
│   │       ├── best_model.pth            # Best validation checkpoint (27.5 MB)
│   │       └── model_config.json         # Class mapping & normalization metadata
│   ├── data/                             # Leaf datasets & botanical metadata
│   │   ├── leaf_processed/               # Split dataset (train/val/test)
│   │   └── medicinal_plants_metadata.json# Botanical database
│   ├── train.py                          # Training script with Cosine Annealing
│   ├── evaluate.py                       # Model evaluation & confusion matrix generator
│   └── requirements.txt                  # Standalone ML dependencies
├── prescription_ocr/                     # Clinical Prescription OCR Subsystem
│   ├── ocr_engine.py                     # EasyOCR reader & line clustering
│   ├── medicine_extractor.py             # Regex entity parser for dosages/instructions
│   ├── preprocessing.py                  # Contrast enhancement (CLAHE) & resolution bounds
│   └── schemas.py                        # Pydantic data schemas
├── pill_identification/                  # Pill Identification Inference Subsystem
│   ├── predictor.py                      # Single-pass MobileNetV2 feature extractor
│   ├── preprocessing.py                  # Pill image preprocessor
│   └── schemas.py                        # Pill data schemas
├── pill_training/                        # Pill Model Training Subsystem
│   ├── models/                           # Trained pill model checkpoints
│   │   └── pill_training_20260921_125546/# Active pill model artifact directory
│   │       ├── final_model.pth           # Trained weights (10.5 MB)
│   │       └── model_config.json         # Class mappings & NDC metadata
│   ├── prepare_dataset.py                # Few-shot dataset splitter & validator
│   └── train.py                          # Pill transfer learning trainer
├── datasets/                             # Raw Datasets
│   ├── handwritten_pages_jpg/            # 30 real clinical prescription scans
│   └── small_dataset_20_images/          # 20 reference pill classes (ePillID benchmark)
├── Medicine/                             # React + Vite Frontend Application
│   ├── src/                              # Components, Pages, Context, & API services
│   │   ├── services/api.js               # Unified Axios API client
│   │   ├── pages/                        # LeafDetection, PrescriptionScan, TabletIdentifier, etc.
│   │   └── components/                   # Navbar, Footer, ResultCards, HistoryModal, etc.
│   ├── package.json                      # Frontend dependency manifest
│   └── vite.config.js                    # Vite server configuration & API proxy
├── main.py                               # Root ASGI entrypoint runner
├── requirements.txt                      # Root Python dependencies
├── .env.example                          # Environment variable configuration template
├── test_end_to_end.py                    # 28-test comprehensive regression suite
├── test_security.py                      # 26-test OWASP security verification suite
└── benchmark_performance.py              # Performance profiling script
```

---

## 5. ML Models

### Model 1: Medicinal Leaf Classifier (`MobileNetV2`)
- **Backbone:** MobileNetV2 pre-trained on ImageNet.
- **Custom Head:** `Dropout(p=0.2) -> Linear(in_features=1280, out_features=6)`.
- **Target Classes (6 species):**
  1. `Centella Asiatica` (Gotu Kola)
  2. `Coccinia Grandis` (Ivy Gourd / Tindora)
  3. `Eclipta Prostrata` (Bhringraj / False Daisy)
  4. `Mikania Micrantha` (Bitter Vine)
  5. `Murraya koenigii` (Curry Leaf / Kadi Patta)
  6. `Stephania Japonica` (Snake Needle Grass)
- **Input Size:** $3 \times 224 \times 224$, normalized with ImageNet mean `[0.485, 0.456, 0.406]` and std `[0.229, 0.224, 0.225]`.

### Model 2: Prescription OCR Engine (`EasyOCR + NLP Parser`)
- **Text Detection:** CRAFT (Character-Region Awareness for Text Detection).
- **Text Recognition:** Deep CRNN (ResNet + BiLSTM + CTC decoder) configured for English character sets.
- **Image Enhancement Pipeline:** LAB color space Conversion $\rightarrow$ Contrast Limited Adaptive Histogram Equalization (CLAHE) $\rightarrow$ Resolution normalization ($800 \le \text{width} \le 1600$) $\rightarrow$ Edge-preserving smoothing.
- **Entity Extraction:** Heuristic and regex clinical entity parsing matching medicine names, formulations (Tablet, Capsule, Syrup), strengths (mg, mcg, ml), frequency (OD, BD, TDS, QID), and duration (days/weeks).

### Model 3: Pharmaceutical Pill Identifier (`MobileNetV2 + Feature Embeddings`)
- **Architecture:** MobileNetV2 feature extractor generating 1280-dimensional L2-normalized visual embeddings.
- **Classification:** Joint softmax classification coupled with cosine visual similarity matching across the 20 reference drug classes from the ePillID benchmark.

---

## 6. Dataset Information

| Dataset Name | Filesystem Location | Description & Dimensions | Format |
|---|---|---|---|
| **Medicinal Leaves** | `ml_training/data/leaf_processed/` | 1,279 total images across 6 botanical classes (Train: 890, Val: 254, Test: 135) | JPEG/PNG ($224\times 224$) |
| **Handwritten Prescriptions** | `datasets/handwritten_pages_jpg/` | 30 real-world clinical prescription scans containing doctor handwriting, patient headers, Rx symbols, and drug lines | High-res JPEG ($1200\times 1800$) |
| **Pharmaceutical Pills** | `datasets/small_dataset_20_images/` | 20 distinct reference pill formulations from the NIH / ePillID benchmark | RGB JPEG ($224\times 224$) |

---

## 7. Training Process

### Leaf Model Training Pipeline
The leaf classifier was trained using transfer learning with dynamic data augmentation:
- **Augmentation Suite:** `RandomResizedCrop(224, scale=(0.8, 1.0))`, `RandomHorizontalFlip(p=0.5)`, `RandomVerticalFlip(p=0.5)`, `RandomRotation(degrees=30)`, and `ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2)`.
- **Optimizer:** AdamW (`lr=0.0003`, `weight_decay=0.01`).
- **Scheduler:** `CosineAnnealingLR` over 15 epochs.
- **Loss Function:** Class-weighted `CrossEntropyLoss` compensating for slight dataset distribution variance.
- **Execution Script:** `python ml_training/train.py`

### Pill Model Training Pipeline
The pill classifier was fine-tuned on the reference pill benchmark using stratified split validation:
- **Optimizer:** AdamW (`lr=0.0005`, `weight_decay=0.0001`).
- **Scheduler:** `CosineAnnealingLR` over 20 epochs.
- **Execution Script:** `python pill_training/train.py`

---

## 8. Model Evaluation

### Leaf Classifier Benchmark Metrics
Evaluated on the independent 135-sample test set (`ml_training/evaluate.py`):
- **Test Accuracy:** **97.04%** (131 / 135 correctly classified)
- **Macro Precision:** **0.9715**
- **Macro Recall:** **0.9698**
- **Macro F1-Score:** **0.9702**

| Plant Class | Precision | Recall | F1-Score | Test Samples |
|---|---|---|---|---|
| *Centella Asiatica* | 1.0000 | 0.9524 | 0.9756 | 21 |
| *Coccinia Grandis* | 0.9524 | 0.9524 | 0.9524 | 21 |
| *Eclipta Prostrata* | 0.9583 | 1.0000 | 0.9787 | 23 |
| *Mikania Micrantha* | 1.0000 | 0.9545 | 0.9767 | 22 |
| *Murraya koenigii* | 0.9231 | 1.0000 | 0.9600 | 24 |
| *Stephania Japonica* | 1.0000 | 0.9583 | 0.9787 | 24 |

---

## 9. FastAPI Backend

The backend is built with FastAPI and designed for zero cold-start latency and strict security compliance:

- **Lifespan Initialization (`@asynccontextmanager`):** AI models and database metadata are preloaded into memory once at application launch. Dummy tensors are passed through PyTorch models to compile operator graphs before serving client traffic.
- **Security Validation Layer (`backend/security.py`):**
  - Filename sanitization preventing path traversal (`../../`).
  - Magic byte binary inspection intercepting spoofed binaries.
  - Stream chunking (64 KB buffers) rejecting payloads $> 15\text{ MB}$ with `HTTP 413`.
  - PIL decompression bomb threshold set to `50_000_000` pixels.
  - Error message path scrubber removing local filesystem references (`C:\...` or `/...`).

---

## 10. API Endpoints

### 1. Leaf Prediction
- **`POST /predict/leaf`** (Aliases: `/api/predict/leaf`, `/api/leaf/predict`)
- **Request:** `multipart/form-data` with `file` or `image`
- **Response:**
  ```json
  {
    "success": true,
    "requestId": "req_1726912345678",
    "message": "Medicinal leaf prediction completed.",
    "data": {
      "id": "leaf_1726912345678",
      "plant": {
        "id": 1,
        "name": "Centella Asiatica",
        "scientificName": "Centella asiatica",
        "family": "Apiaceae",
        "uses": ["Cognitive enhancement", "Wound healing", "Skin repair"],
        "activeCompounds": ["Asiaticoside", "Madecassoside", "Asiatic acid"],
        "precautions": ["Avoid in high doses during pregnancy"]
      },
      "confidence": 99.2,
      "confidence_percent": "99.20%",
      "topPredictions": [
        {"name": "Centella Asiatica", "confidence": 99.2, "confidence_percent": "99.20%"},
        {"name": "Coccinia Grandis", "confidence": 0.5, "confidence_percent": "0.50%"},
        {"name": "Eclipta Prostrata", "confidence": 0.3, "confidence_percent": "0.30%"}
      ],
      "status": "success",
      "inferenceTimeMs": 108.8
    }
  }
  ```

### 2. Prescription OCR
- **`POST /predict/prescription`** (Aliases: `/api/predict/prescription`, `/api/prescription/scan`)
- **Request:** `multipart/form-data` with `file` or `image`
- **Response:**
  ```json
  {
    "success": true,
    "requestId": "req_1726912345678",
    "message": "Prescription scanned successfully.",
    "data": {
      "id": "rx_1726912345678",
      "isHandwritten": true,
      "prescriptionNumber": "RX-4821",
      "patientName": "John Doe",
      "patientAge": "45",
      "patientSex": "Male",
      "doctorName": "Dr. Sarah Jenkins",
      "organization": "St. Jude Medical Center",
      "medicines": [
        {
          "medicineName": "Amoxicillin",
          "dosage": "500 mg",
          "frequency": "Three times daily (TDS)",
          "duration": "7 days",
          "instructions": "Take after meals",
          "form": "Capsule",
          "confidence": 94.5
        }
      ],
      "extractedText": "Rx Amoxicillin 500mg TDS 7 days...",
      "overallConfidence": 91.2,
      "processingTimeMs": 6450.0
    }
  }
  ```

### 3. Pill Identification
- **`POST /predict/pill`** (Aliases: `/api/predict/pill`, `/api/tablet/predict`)
- **Request:** `multipart/form-data` with `file` or `image`
- **Response:**
  ```json
  {
    "success": true,
    "requestId": "req_1726912345678",
    "message": "Pharmaceutical tablet prediction completed.",
    "data": {
      "id": "tablet_1726912345678",
      "medicine": {
        "id": "med-001",
        "name": "Clozaril",
        "genericName": "Clozapine",
        "category": "Atypical Antipsychotic",
        "dosage": "100 mg",
        "manufacturer": "Novartis Pharmaceuticals"
      },
      "confidence": 98.4,
      "topPredictions": [
        {"name": "Clozaril", "genericName": "Clozapine", "strength": "100 mg", "confidence": 98.4}
      ],
      "status": "success",
      "inferenceTimeMs": 52.0
    }
  }
  ```

### 4. Metadata & Utility Endpoints
- **`GET /health`** — Health check reporting status of all inference services.
- **`GET /plants/details?name={name}`** — Botanical search by scientific or common name.
- **`GET /medicines/details?name={name}`** — Pharmacology monograph lookup.
- **`GET /history`** — Session detection history.

---

## 11. Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd Medicine
   ```
2. **Install Node modules:**
   ```bash
   npm install
   ```
3. **Configuration:**
   The frontend automatically proxies `/predict`, `/api`, `/plants`, `/medicines`, and `/history` to `http://127.0.0.1:8000` via [Medicine/vite.config.js](file:///c:/Users/Harshu/Desktop/Medicine/Medicine/vite.config.js).

---

## 12. Backend Setup

1. **Create and activate a Python virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create local environment file:**
   ```bash
   cp .env.example .env
   ```

---

## 13. Environment Variables

Defined in `.env` (refer to [.env.example](file:///c:/Users/Harshu/Desktop/Medicine/.env.example)):

| Variable | Type | Default | Description |
|---|---|---|---|
| `ENVIRONMENT` | string | `development` | Runtime mode (`development`, `staging`, `production`) |
| `HOST` | string | `127.0.0.1` | Host address to bind the Uvicorn server |
| `PORT` | integer | `8000` | Port for the FastAPI backend server |
| `MAX_UPLOAD_SIZE_MB` | integer | `15` | Maximum upload size threshold in Megabytes |
| `CORS_ORIGINS` | string | `http://localhost:5173,...` | Comma-separated list of allowed CORS origins |
| `LOG_LEVEL` | string | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `OCR_LANGUAGES` | string | `en` | Comma-separated OCR recognition languages |
| `OCR_USE_GPU` | boolean | `false` | Enable CUDA acceleration for EasyOCR if GPU is available |

---

## 14. How to Run the Project

### Start the Complete System (2 Terminals)

#### Terminal 1 — Start Backend Server:
```bash
# From workspace root
python main.py
# Or using Uvicorn CLI
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Server: `http://127.0.0.1:8000`
- Interactive Documentation: `http://127.0.0.1:8000/docs`

#### Terminal 2 — Start Frontend Application:
```bash
cd Medicine
npm run dev
```
- Web Application: `http://localhost:5173`

---

## 15. How to Test the APIs

The codebase contains three automated test suites:

### 1. Full End-to-End Regression Suite (28 Tests)
Verifies real predictions across all 6 plant species, authentic prescriptions, pill samples, 0-byte files, corrupted uploads, and concurrency:
```bash
python test_end_to_end.py
```

### 2. OWASP Security & Validation Suite (26 Tests)
Validates path traversal resistance, magic byte enforcement, extension whitelisting, decompression bomb protection, and error message sanitization:
```bash
python test_security.py
```

### 3. Performance & Latency Benchmark Suite
Measures round-trip API latencies and server ML inference times:
```bash
python benchmark_performance.py
```

---

## 16. How to Train Models

> [!NOTE]
> The production application runs pre-trained model checkpoints. The training steps below are only required when re-training models on updated datasets.

### 1. Retrain the Leaf Classification Model
```bash
# 1. Install ML training requirements
pip install -r ml_training/requirements.txt

# 2. Run the training pipeline
python ml_training/train.py

# 3. Evaluate the newly trained checkpoint
python ml_training/evaluate.py
```

### 2. Retrain the Pill Identification Model
```bash
# 1. Prepare and validate the few-shot pill dataset
python pill_training/prepare_dataset.py

# 2. Run the transfer learning trainer
python pill_training/train.py
```

---

## 17. Where Trained Checkpoints are Stored

All model checkpoints and configuration files are versioned in dedicated directories:

| Component | Weights File | Architecture & Class Metadata |
|---|---|---|
| **Leaf Classification** | `ml_training/models/training_20260919_135002/final_model.pth` | `ml_training/models/training_20260919_135002/model_config.json` |
| **Pill Identification** | `pill_training/models/pill_training_20260921_125546/final_model.pth` | `pill_training/models/pill_training_20260921_125546/model_config.json` |
| **Plant Knowledge Base** | `ml_training/data/medicinal_plants_metadata.json` | Botanical database loaded into RAM |
| **EasyOCR Weights** | Standard PyTorch hub cache directory (`~/.EasyOCR/`) | CRAFT & CRNN pre-trained models |

---

## 18. Troubleshooting

### 1. CORS or Network Errors in the Frontend
- Ensure the backend server is running on `http://127.0.0.1:8000`.
- Verify `CORS_ORIGINS` in `.env` includes `http://localhost:5173` or is set to `*`.

### 2. `UnidentifiedImageError` or `CorruptedImageError` on Upload
- The security validation layer strictly requires valid image headers. Verify that uploaded files are authentic JPEG, PNG, WEBP, BMP, or TIFF images.

### 3. PyTorch CPU vs. CUDA Warning
- The application defaults to CPU inference (`device: cpu`). If a CUDA-enabled GPU is available and `torch.cuda.is_available()` evaluates to `True`, the services automatically switch to GPU execution.

### 4. EasyOCR Model Download Delay on First Launch
- On the very first run, EasyOCR downloads the detection and recognition neural network weights (~100 MB). Subsequent server startups load instantly from the local cache.

---

## 19. Known Limitations

1. **OCR on Extremely Cursive Handwriting:** While the OCR pipeline accurately parses semi-legible doctor handwriting and printed prescriptions, severely degraded or non-standard cursive scripts may produce lower confidence entity extractions.
2. **Leaf Class Domain:** The leaf classification model is trained on 6 specific authentic medicinal species (*Centella Asiatica*, *Coccinia Grandis*, *Eclipta Prostrata*, *Mikania Micrantha*, *Murraya koenigii*, *Stephania Japonica*). Uploading unrelated non-medicinal flora will be categorized against the closest botanical feature candidate.
3. **In-Memory History:** Detection history is maintained in RAM for session speed and privacy; restarting the backend resets the session history unless integrated with a persistent SQL database.
