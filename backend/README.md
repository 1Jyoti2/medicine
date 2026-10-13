# Medicine AI — FastAPI Modular Backend

Production-grade, clean modular FastAPI architecture for the Medicine AI backend.

---

## Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI Application initialization, lifespan & exception guards
│   │
│   ├── api/                      # API Router & Endpoints
│   │   ├── __init__.py
│   │   ├── router.py             # Root API router aggregator
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── leaf.py           # POST /predict/leaf endpoints
│   │       ├── pill.py           # POST /predict/pill endpoints
│   │       ├── prescription.py   # POST /predict/prescription endpoints
│   │       ├── metadata.py       # GET /plants/details, /medicines/details, /history
│   │       └── health.py         # GET /health health check
│   │
│   ├── core/                     # Core Configuration & Security
│   │   ├── __init__.py
│   │   ├── config.py             # Pydantic / Typed settings from .env
│   │   └── security.py           # Magic bytes, stream limiters, path sanitization
│   │
│   ├── db/                       # Database & Session Management
│   │   ├── __init__.py
│   │   ├── database.py           # SQLAlchemy engine & Base declarative model
│   │   └── session.py            # SessionLocal & get_db FastAPI dependency
│   │
│   ├── models/                   # Database ORM Models
│   │   ├── __init__.py
│   │   ├── plant.py              # PlantModel
│   │   ├── medicine.py           # MedicineModel
│   │   └── history.py            # HistoryModel
│   │
│   ├── schemas/                  # Pydantic Request & Response Envelopes
│   │   ├── __init__.py
│   │   ├── common.py             # ApiResponse & ErrorResponse
│   │   ├── leaf.py               # LeafPredictionResult, PlantProfile
│   │   ├── pill.py               # PillPredictionResult, MedicineProfile
│   │   ├── prescription.py       # PrescriptionScanResult, PrescribedMedicine
│   │   └── metadata.py           # HistoryItem, HealthStatus
│   │
│   └── services/                 # Business Logic & ML Service Integrations
│       ├── __init__.py
│       ├── leaf_service.py       # LeafClassifier coordination
│       ├── pill_service.py       # PillClassifier coordination
│       ├── prescription_service.py # PrescriptionPipeline coordination
│       └── metadata_service.py   # Knowledge bases & history storage
│
├── .env                          # Local environment variables
├── .env.example                  # Environment configuration template
├── .gitignore                    # Backend gitignore (.env, *.db)
├── main.py                       # Backward-compatibility runner
├── requirements.txt              # Backend dependencies
└── README.md                     # Backend documentation
```

---

## Running the Backend

From the workspace root directory:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
Or directly:
```bash
python main.py
```

- **Interactive API Documentation:** `http://127.0.0.1:8000/docs`
- **Health Check Endpoint:** `http://127.0.0.1:8000/health`
