"""
Metadata and History Storage Service.
Integrates PostgreSQL database operations with in-memory caching and fallback.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from backend.app.core.config import settings
from backend.app.db.database import check_db_connection, init_db
from backend.app.db.session import SessionLocal

logger = logging.getLogger("medicine.backend.services.metadata")

# In-Memory Fallback & Cache Repositories
PLANTS_DB: Dict[str, Any] = {}
MEDICINES_DB: Dict[str, Any] = {}
HISTORY_STORE: List[Dict[str, Any]] = []


def load_databases():
    """
    Initializes database tables, syncs metadata to PostgreSQL, and preloads cache.
    """
    global PLANTS_DB, MEDICINES_DB

    # 1. Initialize Tables
    init_db()

    # 2. Load Medicinal Plants Metadata from JSON
    meta_path = settings.ML_TRAINING_DIR / "data" / "medicinal_plants_metadata.json"
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                PLANTS_DB = json.load(f)
            logger.info(f"Loaded {len(PLANTS_DB)} medicinal plants into memory cache.")
        except Exception as e:
            logger.warning(f"Failed to load plants metadata file: {e}")

    # Fallback / Default Plant Profiles
    default_plants = {
        "Centella Asiatica": {
            "id": 1,
            "name": "Centella Asiatica",
            "scientificName": "Centella asiatica",
            "family": "Apiaceae",
            "nativeRegion": "Asia (India, Sri Lanka, China)",
            "imageUrl": "/images/plants/centella-asiatica.jpg",
            "uses": ["Cognitive enhancement", "Wound healing", "Skin repair", "Anxiety & stress reduction"],
            "activeCompounds": ["Asiaticoside", "Madecassoside", "Asiatic acid", "Flavonoids"],
            "partsUsed": "Whole plant, leaves",
            "precautions": ["Avoid in high doses during pregnancy", "Consult doctor before surgery"],
            "sideEffects": ["Mild stomach upset", "Drowsiness"],
            "description": "Centella asiatica (Gotu Kola) is a renowned Ayurvedic herb for brain health, memory enhancement, and dermatological healing.",
            "remedies": [
                {
                    "name": "Gotu Kola Memory & Vitality Tonic",
                    "ingredients": ["Fresh Centella Asiatica leaves", "Warm water or milk", "Honey (optional)"],
                    "preparation": "Crush fresh leaves to extract 10-15 ml of pure juice. Mix with warm water or milk and honey. Consume in the morning.",
                    "traditionalUse": "Ayurvedic Medhya Rasayana beverage traditionally taken for memory retention, mental clarity, and nerve health.",
                    "precautions": "Avoid excessive intake. Discontinue if gastric discomfort occurs."
                },
                {
                    "name": "Gotu Kola Skin Soothing Paste",
                    "ingredients": ["Fresh Centella leaves", "Rose water or clean water"],
                    "preparation": "Grind fresh leaves into a fine paste. Apply evenly to minor blemishes or irritated skin areas for 15-20 minutes, then rinse.",
                    "traditionalUse": "Traditional topical preparation used to promote skin revitalization and accelerate soothing.",
                    "precautions": "Do not apply to deep open wounds. Perform a skin patch test first."
                }
            ]
        },
        "Coccinia Grandis": {
            "id": 2,
            "name": "Coccinia Grandis",
            "scientificName": "Coccinia grandis",
            "family": "Cucurbitaceae",
            "nativeRegion": "Tropical Asia and Africa",
            "imageUrl": "/images/plants/coccinia-grandis.jpg",
            "uses": ["Blood sugar regulation", "Anti-inflammatory", "Antioxidant support", "Liver protection"],
            "activeCompounds": ["Cephalandrin", "Beta-carotene", "Flavonoids", "Vitamin C"],
            "partsUsed": "Leaves and fruits",
            "precautions": ["Monitor blood glucose if taking diabetes medication"],
            "sideEffects": ["Hypoglycemia if combined with insulin"],
            "description": "Coccinia grandis (Ivy Gourd / Tindora) is traditionally used in Ayurvedic medicine for managing diabetes and metabolic health.",
            "remedies": [
                {
                    "name": "Ivy Gourd Leaf Infusion for Blood Sugar",
                    "ingredients": ["Fresh Coccinia Grandis leaves", "Water", "Cumin seeds (optional)"],
                    "preparation": "Boil a handful of washed fresh leaves in two cups of water with a pinch of cumin seeds for 5 minutes. Strain and drink warm before meals.",
                    "traditionalUse": "Traditional Ayurvedic preparation consumed to support healthy glycemic balance and metabolic wellness.",
                    "precautions": "Monitor blood sugar levels regularly if taking antidiabetic medication to prevent hypoglycemia."
                },
                {
                    "name": "Cooling Coccinia Leaf Juice",
                    "ingredients": ["Fresh Coccinia leaves", "Water", "Pinch of black salt"],
                    "preparation": "Blend washed tender leaves with half a cup of water, strain, add a pinch of black salt, and drink fresh.",
                    "traditionalUse": "Traditional cooling tonic used to alleviate internal body heat and promote skin wellness.",
                    "precautions": "Consume freshly prepared; do not store overnight."
                }
            ]
        },
        "Eclipta Prostrata": {
            "id": 3,
            "name": "Eclipta Prostrata",
            "scientificName": "Eclipta prostrata",
            "family": "Asteraceae",
            "nativeRegion": "Tropical & Subtropical regions",
            "imageUrl": "/images/plants/eclipta-prostrata.jpg",
            "uses": ["Hair growth & vitality", "Liver rejuvenation", "Skin wellness", "Antimicrobial"],
            "activeCompounds": ["Wedelolactone", "Demethylwedelolactone", "Ecliptine", "Flavonoids"],
            "partsUsed": "Leaves and whole herb",
            "precautions": ["Avoid during pregnancy without medical consultation"],
            "sideEffects": ["Mild chilliness in sensitive individuals"],
            "description": "Eclipta prostrata (Bhringraj) is the 'King of Herbs' for hair nourishment, liver detoxification, and vitality in Ayurveda.",
            "remedies": [
                {
                    "name": "Bhringraj Ayurvedic Hair Oil",
                    "ingredients": ["Fresh Eclipta Prostrata leaf juice", "Pure virgin coconut oil or sesame oil"],
                    "preparation": "Simmer equal parts fresh leaf juice and coconut oil on low heat until moisture evaporates and dark green herbal oil remains. Cool and strain into a glass bottle.",
                    "traditionalUse": "Renowned Ayurvedic hair oil massaged into the scalp to strengthen roots, prevent premature greying, and stimulate hair vitality.",
                    "precautions": "For external scalp application only. Perform a skin patch test."
                },
                {
                    "name": "Bhringraj Leaf Liver Wellness Brew",
                    "ingredients": ["Dried Bhringraj herb", "Water"],
                    "preparation": "Boil 3g of dried whole herb in a cup of water for 5 minutes. Strain and consume lukewarm.",
                    "traditionalUse": "Traditional herbal brew historically used for liver rejuvenation and natural detoxification.",
                    "precautions": "Consult an Ayurvedic practitioner before internal use."
                }
            ]
        },
        "Mikania Micrantha": {
            "id": 4,
            "name": "Mikania Micrantha",
            "scientificName": "Mikania micrantha",
            "family": "Asteraceae",
            "nativeRegion": "Central and South America, naturalized in Asia",
            "imageUrl": "/images/plants/mikania-micrantha.jpg",
            "uses": ["Wound healing & clotting", "Antibacterial", "Fever reduction", "Pain relief"],
            "activeCompounds": ["Mikanolide", "Dihydromikanolide", "Sesquiterpene lactones"],
            "partsUsed": "Leaves",
            "precautions": ["External application preferred; internal use only under guidance"],
            "sideEffects": ["Skin dermatitis in rare allergic individuals"],
            "description": "Mikania micrantha (Bitter Vine) is traditionally applied topically as a rapid coagulant and antiseptic on acute wounds.",
            "remedies": [
                {
                    "name": "Fresh Mikania Wound Poultice",
                    "ingredients": ["Fresh Mikania Micrantha leaves"],
                    "preparation": "Wash fresh tender leaves thoroughly. Crush between palms or with a pestle to release herbal juice. Apply directly onto minor cuts, scratches, or insect bites.",
                    "traditionalUse": "Traditional rapid styptic and antiseptic poultice used in rural areas to arrest minor bleeding and soothe wounds.",
                    "precautions": "Ensure leaves are thoroughly clean. Seek professional medical care for deep wounds."
                },
                {
                    "name": "Mikania Herbal Steam Inhalation",
                    "ingredients": ["Fresh Mikania leaves", "Boiling water"],
                    "preparation": "Add a handful of leaves to a bowl of steaming water. Cover head with a towel and inhale herbal vapors for 5-10 minutes.",
                    "traditionalUse": "Traditional respiratory steam used for clearing nasal passages and soothing throat irritation.",
                    "precautions": "Keep a safe distance to avoid steam burns."
                }
            ]
        },
        "Murraya koenigii": {
            "id": 5,
            "name": "Murraya koenigii",
            "scientificName": "Murraya koenigii",
            "family": "Rutaceae",
            "nativeRegion": "Indian subcontinent",
            "imageUrl": "/images/plants/curry-leaves.jpg",
            "uses": ["Digestive support", "Hair health", "Blood sugar management", "Antioxidant booster"],
            "activeCompounds": ["Mahanimbine", "Koenimbine", "Girimbine", "Carbazole alkaloids"],
            "partsUsed": "Fresh leaves",
            "precautions": ["Safe in dietary amounts; consult for therapeutic extracts"],
            "sideEffects": ["None reported in standard dietary use"],
            "description": "Murraya koenigii (Curry Leaves / Kadi Patta) is rich in carbazole alkaloids supporting digestive fire, glycemic balance, and hair pigments.",
            "remedies": [
                {
                    "name": "Curry Leaf Digestive Buttermilk",
                    "ingredients": ["Fresh curry leaves", "Fresh buttermilk", "Roasted cumin powder", "Pinch of rock salt"],
                    "preparation": "Finely crush 8-10 fresh curry leaves and stir into a glass of spiced buttermilk. Drink after lunch.",
                    "traditionalUse": "Ayurvedic digestive drink supporting gut flora, appetite stimulation, and metabolism.",
                    "precautions": "Safe in standard dietary usage."
                },
                {
                    "name": "Curry Leaf & Fenugreek Hair Mask",
                    "ingredients": ["Fresh curry leaves", "Soaked fenugreek seeds", "Yogurt"],
                    "preparation": "Blend leaves and soaked fenugreek seeds into a smooth paste with yogurt. Apply to scalp for 25 minutes, then rinse.",
                    "traditionalUse": "Traditional hair care mask promoting follicular health and reducing dandruff.",
                    "precautions": "For external scalp use only."
                }
            ]
        },
        "Stephania Japonica": {
            "id": 6,
            "name": "Stephania Japonica",
            "scientificName": "Stephania japonica",
            "family": "Menispermaceae",
            "nativeRegion": "East and South Asia, Australasia",
            "imageUrl": "/images/plants/stephania-japonica.jpg",
            "uses": ["Joint pain relief", "Anti-inflammatory", "Anti-rheumatic", "Fever management"],
            "activeCompounds": ["Stepharine", "Hasubanonine", "Metaphanine", "Isoquinoline alkaloids"],
            "partsUsed": "Roots and leaves",
            "precautions": ["Contains potent alkaloids; strictly follow dosage guidelines"],
            "sideEffects": ["Dizziness or nausea with excessive dosage"],
            "description": "Stephania japonica (Snake Needle Grass / Hai Feng Teng) is valued in traditional Asian medicine for rheumatic discomfort and analgesic properties.",
            "remedies": [
                {
                    "name": "Stephania Root Decoction (Joint Relief)",
                    "ingredients": ["Dried Stephania root / stem slices", "Water", "Licorice root (optional)"],
                    "preparation": "Simmer 3-5g of dried root in two cups of water for 15-20 minutes until reduced by half. Strain and drink warm once daily under traditional guidance.",
                    "traditionalUse": "Traditional herbal decoction used in Asian folk traditions for soothing joint stiffness and rheumatic aches.",
                    "precautions": "Contains active isoquinoline alkaloids. Avoid during pregnancy, lactation, or without consulting an herbal practitioner."
                },
                {
                    "name": "Stephania Leaf Warming Poultice",
                    "ingredients": ["Fresh Stephania leaves", "A few drops of sesame oil"],
                    "preparation": "Crush fresh leaves into a poultice and gently warm with a few drops of sesame oil. Apply externally over affected joints or swelling with a clean cloth wrap for 15 minutes.",
                    "traditionalUse": "Traditional external poultice applied to reduce localized joint inflammation and discomfort.",
                    "precautions": "External use only. Test on a small patch of skin first to ensure no irritation."
                }
            ]
        }
    }

    for k, v in default_plants.items():
        if k not in PLANTS_DB:
            PLANTS_DB[k] = v

    # 3. Pharmaceutical Medicines
    MEDICINES_DB = {
        "Clozaril": {
            "id": "med-001",
            "name": "Clozaril",
            "genericName": "Clozapine",
            "category": "Atypical Antipsychotic",
            "composition": "Clozapine 100mg",
            "manufacturer": "Novartis Pharmaceuticals",
            "dosage": "100 mg",
            "storage": "Store below 25°C in a dry place protected from light.",
            "uses": ["Treatment-resistant schizophrenia", "Reducing suicidal behavior"],
            "sideEffects": ["Drowsiness", "Dizziness", "Excessive salivation", "Constipation"],
            "precautions": ["Requires regular absolute neutrophil count (ANC) blood monitoring"],
            "description": "Clozaril (Clozapine) is an atypical antipsychotic indicated for treatment-resistant psychiatric conditions under medical supervision."
        },
        "Divalproex_ER": {
            "id": "med-002",
            "name": "Divalproex Sodium ER",
            "genericName": "Divalproex Sodium",
            "category": "Anticonvulsant / Mood Stabilizer",
            "composition": "Divalproex Sodium Extended-Release 500mg",
            "manufacturer": "Actavis Pharma",
            "dosage": "500 mg",
            "storage": "Store at 20°C to 25°C.",
            "uses": ["Seizure control", "Bipolar manic episodes", "Migraine prophylaxis"],
            "sideEffects": ["Nausea", "Somnolence", "Tremor", "Weight changes"],
            "precautions": ["Monitor liver function tests and platelet counts periodically"],
            "description": "Divalproex Sodium ER is an extended-release anticonvulsant used for mood stabilization and migraine prevention."
        },
        "Ciprofloxacin": {
            "id": "med-003",
            "name": "Ciprofloxacin",
            "genericName": "Ciprofloxacin Hydrochloride",
            "category": "Fluoroquinolone Antibiotic",
            "composition": "Ciprofloxacin 500mg",
            "manufacturer": "Aurobindo Pharma",
            "dosage": "500 mg",
            "storage": "Store in a tightly closed container away from moisture.",
            "uses": ["Bacterial infections", "Urinary tract infections", "Respiratory infections"],
            "sideEffects": ["Nausea", "Diarrhea", "Headache", "Tendon discomfort"],
            "precautions": ["Drink plenty of fluids; avoid concurrent dairy/calcium ingestion"],
            "description": "Ciprofloxacin is a broad-spectrum fluoroquinolone antibiotic targeting susceptible Gram-negative and Gram-positive bacteria."
        },
        "Metformin_ER": {
            "id": "med-004",
            "name": "Metformin ER",
            "genericName": "Metformin Hydrochloride Extended-Release",
            "category": "Antidiabetic (Biguanide)",
            "composition": "Metformin HCl ER 500mg",
            "manufacturer": "Lake Erie Medical",
            "dosage": "500 mg",
            "storage": "Store at room temperature away from excessive heat.",
            "uses": ["Type 2 Diabetes Mellitus glycemic control", "Insulin sensitivity enhancement"],
            "sideEffects": ["Mild gastrointestinal upset", "Metallic taste"],
            "precautions": ["Take with evening meals; monitor renal function periodically"],
            "description": "Metformin ER lowers basal and postprandial blood glucose by improving insulin sensitivity and reducing hepatic gluconeogenesis."
        },
        "Amoxicillin": {
            "id": "med-005",
            "name": "Amoxicillin",
            "genericName": "Amoxicillin Trihydrate",
            "category": "Penicillin Antibiotic",
            "composition": "Amoxicillin 500mg",
            "manufacturer": "Ranbaxy Pharmaceuticals",
            "dosage": "500 mg",
            "storage": "Store in an airtight container below 25°C.",
            "uses": ["Bacterial respiratory infections", "Ear/Nose/Throat infections", "Skin infections"],
            "sideEffects": ["Nausea", "Mild skin rash", "Diarrhea"],
            "precautions": ["Do not use if allergic to penicillin or beta-lactams"],
            "description": "Amoxicillin is a moderate-spectrum bactericidal penicillin antibiotic widely prescribed for acute bacterial infections."
        },
        "Atorvastatin": {
            "id": "med-006",
            "name": "Atorvastatin",
            "genericName": "Atorvastatin Calcium",
            "category": "HMG-CoA Reductase Inhibitor (Statin)",
            "composition": "Atorvastatin 20mg",
            "manufacturer": "St. Marys Medical Park",
            "dosage": "20 mg",
            "storage": "Store at room temperature 20°C to 25°C.",
            "uses": ["Lowering LDL cholesterol and triglycerides", "Reducing cardiovascular risk"],
            "sideEffects": ["Mild muscle aches", "Digestive changes"],
            "precautions": ["Take consistently at bedtime; avoid large quantities of grapefruit juice"],
            "description": "Atorvastatin effectively lowers low-density lipoprotein (LDL) cholesterol and stabilizes atherosclerotic plaques."
        },
        "Omeprazole_DR": {
            "id": "med-007",
            "name": "Omeprazole DR",
            "genericName": "Omeprazole Delayed-Release",
            "category": "Proton Pump Inhibitor (PPI)",
            "composition": "Omeprazole 20mg",
            "manufacturer": "Bryant Ranch Prepack",
            "dosage": "20 mg",
            "storage": "Store in original packaging protected from moisture.",
            "uses": ["Gastroesophageal Reflux Disease (GERD)", "Peptic ulcer healing", "Acid reduction"],
            "sideEffects": ["Headache", "Abdominal discomfort", "Flatulence"],
            "precautions": ["Take 30-60 minutes before breakfast for optimal efficacy"],
            "description": "Omeprazole suppresses gastric acid secretion by specific inhibition of the H+/K+-ATPase proton pump in gastric parietal cells."
        },
        "Amlodipine": {
            "id": "med-008",
            "name": "Amlodipine",
            "genericName": "Amlodipine Besylate",
            "category": "Calcium Channel Blocker",
            "composition": "Amlodipine 10mg",
            "manufacturer": "Direct_Rx",
            "dosage": "10 mg",
            "storage": "Store protected from light and moisture at 15°C to 30°C.",
            "uses": ["Hypertension management", "Coronary artery disease & Angina"],
            "sideEffects": ["Peripheral edema (ankle swelling)", "Flushing", "Dizziness"],
            "precautions": ["Monitor blood pressure regularly; do not discontinue abruptly"],
            "description": "Amlodipine relaxes vascular smooth muscle, dilating coronary and peripheral arterioles to reduce blood pressure."
        }
    }

    # 4. Sync metadata to PostgreSQL if connection is live
    _sync_metadata_to_db()


def _sync_metadata_to_db():
    """Syncs plant and medicine database records to PostgreSQL."""
    if not check_db_connection():
        return

    try:
        from backend.app.models import PlantModel, MedicineModel
        db = SessionLocal()
        try:
            # Sync Plants
            existing_plants = {p[0] for p in db.query(PlantModel.name).all()}
            for plant_name, pdata in PLANTS_DB.items():
                p_actual_name = pdata.get("name", plant_name)
                if p_actual_name not in existing_plants and plant_name not in existing_plants:
                    existing_plants.add(p_actual_name)
                    existing_plants.add(plant_name)
                    plant_rec = PlantModel(
                        name=p_actual_name,
                        scientific_name=pdata.get("scientificName", plant_name),
                        family=pdata.get("family"),
                        native_region=pdata.get("nativeRegion"),
                        image_url=pdata.get("imageUrl"),
                        parts_used=pdata.get("partsUsed"),
                        description=pdata.get("description"),
                        uses=pdata.get("uses", []),
                        active_compounds=pdata.get("activeCompounds", []),
                        precautions=pdata.get("precautions", []),
                        side_effects=pdata.get("sideEffects", []),
                    )
                    db.add(plant_rec)

            # Sync Medicines
            existing_meds = {m[0] for m in db.query(MedicineModel.name).all()}
            existing_ids = {m[0] for m in db.query(MedicineModel.id).all()}
            for med_key, mdata in MEDICINES_DB.items():
                m_actual_name = mdata.get("name", med_key)
                m_id = mdata.get("id", f"med-{med_key}")
                if m_actual_name not in existing_meds and m_id not in existing_ids:
                    existing_meds.add(m_actual_name)
                    existing_ids.add(m_id)
                    med_rec = MedicineModel(
                        id=m_id,
                        name=m_actual_name,
                        generic_name=mdata.get("genericName", med_key),
                        category=mdata.get("category"),
                        composition=mdata.get("composition"),
                        manufacturer=mdata.get("manufacturer"),
                        dosage=mdata.get("dosage"),
                        storage=mdata.get("storage"),
                        description=mdata.get("description"),
                        uses=mdata.get("uses", []),
                        side_effects=mdata.get("sideEffects", []),
                        precautions=mdata.get("precautions", []),
                    )
                    db.add(med_rec)

            db.commit()
            logger.info("Successfully synced metadata records to PostgreSQL database.")
        except Exception as e:
            db.rollback()
            logger.warning(f"Metadata DB sync skipped: {e}")
        finally:
            db.close()
    except Exception as e:
        logger.warning(f"Error during metadata DB sync: {e}")


def get_plant_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Retrieve plant details from DB or memory cache."""
    name_clean = name.strip().lower()

    # Try PostgreSQL first if available
    if check_db_connection():
        try:
            from backend.app.models import PlantModel
            db = SessionLocal()
            try:
                plant = db.query(PlantModel).filter(
                    (PlantModel.name.ilike(name.strip())) | 
                    (PlantModel.scientific_name.ilike(name.strip()))
                ).first()
                if plant:
                    return {
                        "id": plant.id,
                        "name": plant.name,
                        "scientificName": plant.scientific_name,
                        "family": plant.family,
                        "nativeRegion": plant.native_region,
                        "imageUrl": plant.image_url,
                        "uses": plant.uses or [],
                        "activeCompounds": plant.active_compounds or [],
                        "partsUsed": plant.parts_used,
                        "precautions": plant.precautions or [],
                        "sideEffects": plant.side_effects or [],
                        "description": plant.description
                    }
            finally:
                db.close()
        except Exception as e:
            logger.debug(f"DB plant query error: {e}")

    # Memory cache fallback
    for plant_key, plant in PLANTS_DB.items():
        if (plant_key.lower() == name_clean or 
            plant.get("name", "").lower() == name_clean or 
            plant.get("scientificName", "").lower() == name_clean):
            return plant

    for plant_key, plant in PLANTS_DB.items():
        if name_clean in plant_key.lower() or name_clean in plant.get("name", "").lower():
            return plant
    return None


def get_medicine_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Retrieve medicine details from DB or memory cache."""
    name_clean = name.strip().lower()

    if check_db_connection():
        try:
            from backend.app.models import MedicineModel
            db = SessionLocal()
            try:
                med = db.query(MedicineModel).filter(
                    (MedicineModel.name.ilike(name.strip())) | 
                    (MedicineModel.generic_name.ilike(name.strip()))
                ).first()
                if med:
                    return {
                        "id": med.id,
                        "name": med.name,
                        "genericName": med.generic_name,
                        "category": med.category,
                        "composition": med.composition,
                        "manufacturer": med.manufacturer,
                        "dosage": med.dosage,
                        "storage": med.storage,
                        "uses": med.uses or [],
                        "sideEffects": med.side_effects or [],
                        "precautions": med.precautions or [],
                        "description": med.description
                    }
            finally:
                db.close()
        except Exception as e:
            logger.debug(f"DB medicine query error: {e}")

    for med_key, med in MEDICINES_DB.items():
        if (med_key.lower() == name_clean or 
            med.get("name", "").lower() == name_clean or 
            med.get("genericName", "").lower() == name_clean):
            return med

    for med_key, med in MEDICINES_DB.items():
        if name_clean in med_key.lower() or name_clean in med.get("name", "").lower():
            return med
    return None


def record_history(item: Dict[str, Any]):
    """Records detection scan in memory and persists to PostgreSQL."""
    HISTORY_STORE.insert(0, item)

    if check_db_connection():
        try:
            from backend.app.models import HistoryModel
            db = SessionLocal()
            try:
                hist_rec = HistoryModel(
                    id=item.get("id"),
                    name=item.get("name", "Scan Result"),
                    type=item.get("type", "Detection"),
                    confidence=float(item.get("confidence", 0.0)),
                    date=item.get("date", ""),
                    status=item.get("status", "processed"),
                    result_id=item.get("resultId", item.get("id"))
                )
                db.add(hist_rec)
                db.commit()
            except Exception as e:
                db.rollback()
                logger.warning(f"History record DB persistence error: {e}")
            finally:
                db.close()
        except Exception as e:
            logger.warning(f"Error persisting history: {e}")


def get_all_history() -> List[Dict[str, Any]]:
    """Retrieves history from PostgreSQL or in-memory store."""
    if check_db_connection():
        try:
            from backend.app.models import HistoryModel
            db = SessionLocal()
            try:
                records = db.query(HistoryModel).order_by(HistoryModel.created_at.desc()).limit(100).all()
                if records:
                    return [
                        {
                            "id": r.id,
                            "name": r.name,
                            "type": r.type,
                            "confidence": r.confidence,
                            "date": r.date,
                            "status": r.status,
                            "resultId": r.result_id
                        }
                        for r in records
                    ]
            finally:
                db.close()
        except Exception as e:
            logger.debug(f"DB history query error: {e}")

    return HISTORY_STORE
