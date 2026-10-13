"""
Dataset preparation for Pill Identification.
Organizes the 20 raw ePillID pill images into structured splits (Train, Val, Test)
with strict zero data leakage, reproducible random seeding, and metadata tagging.
"""

import json
import os
import shutil
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np

# Random seed for exact reproducibility
RANDOM_SEED = 42

NDC_METADATA = {
    "0078-0489": {
        "class_name": "Clozaril",
        "generic_name": "Clozapine",
        "strength": "100 mg",
        "form": "Tablet",
        "manufacturer": "Novartis Pharmaceuticals",
        "description": "Yellow round tablet used for treatment-resistant schizophrenia."
    },
    "0591-5786": {
        "class_name": "Divalproex_ER",
        "generic_name": "Divalproex Sodium Extended-Release",
        "strength": "500 mg",
        "form": "Tablet",
        "manufacturer": "Actavis Pharma",
        "description": "Oval white film-coated tablet for seizure and bipolar disorder."
    },
    "12634-604": {
        "class_name": "Ciprofloxacin",
        "generic_name": "Ciprofloxacin Hydrochloride",
        "strength": "500 mg",
        "form": "Tablet",
        "manufacturer": "Aurobindo Pharma",
        "description": "White oblong film-coated antibiotic tablet."
    },
    "35356-718": {
        "class_name": "Metformin_ER",
        "generic_name": "Metformin Hydrochloride Extended-Release",
        "strength": "500 mg",
        "form": "Tablet",
        "manufacturer": "Lake Erie Medical",
        "description": "White round extended-release tablet for type 2 diabetes."
    },
    "48433-316": {
        "class_name": "Amoxicillin",
        "generic_name": "Amoxicillin Trihydrate",
        "strength": "500 mg",
        "form": "Capsule",
        "manufacturer": "Ranbaxy Pharmaceuticals",
        "description": "Pink and blue capsule for bacterial infections."
    },
    "50436-2948": {
        "class_name": "Hydrochlorothiazide",
        "generic_name": "Hydrochlorothiazide",
        "strength": "25 mg",
        "form": "Tablet",
        "manufacturer": "Unit Dose Services",
        "description": "Light yellow round scored tablet for hypertension and edema."
    },
    "55154-7271": {
        "class_name": "Lisinopril",
        "generic_name": "Lisinopril",
        "strength": "20 mg",
        "form": "Tablet",
        "manufacturer": "Cardinal Health",
        "description": "Round pink tablet for high blood pressure and heart failure."
    },
    "60760-266": {
        "class_name": "Atorvastatin",
        "generic_name": "Atorvastatin Calcium",
        "strength": "20 mg",
        "form": "Tablet",
        "manufacturer": "St. Marys Medical Park",
        "description": "White elliptical tablet for cholesterol management."
    },
    "61786-419": {
        "class_name": "Omeprazole_DR",
        "generic_name": "Omeprazole Delayed-Release",
        "strength": "20 mg",
        "form": "Capsule",
        "manufacturer": "Bryant Ranch Prepack",
        "description": "Delayed-release capsule for GERD and acid reflux."
    },
    "61919-317": {
        "class_name": "Amlodipine",
        "generic_name": "Amlodipine Besylate",
        "strength": "10 mg",
        "form": "Tablet",
        "manufacturer": "Direct_Rx",
        "description": "White octagon-shaped tablet for hypertension and angina."
    },
    "68084-344": {
        "class_name": "Levothyroxine",
        "generic_name": "Levothyroxine Sodium",
        "strength": "50 mcg",
        "form": "Tablet",
        "manufacturer": "American Health Packaging",
        "description": "Round white scored tablet for hypothyroidism."
    },
    "68084-520": {
        "class_name": "Metoprolol_Tartrate",
        "generic_name": "Metoprolol Tartrate",
        "strength": "50 mg",
        "form": "Tablet",
        "manufacturer": "American Health Packaging",
        "description": "Round pink scored tablet for high blood pressure and heart rate."
    },
    "69189-0468": {
        "class_name": "Sertraline",
        "generic_name": "Sertraline Hydrochloride",
        "strength": "50 mg",
        "form": "Tablet",
        "manufacturer": "Bryant Ranch Prepack",
        "description": "Blue capsule-shaped tablet for depression, anxiety, and OCD."
    },
    "1450": {
        "class_name": "Pill_Ref_1450",
        "generic_name": "Pharmaceutical Reference Sample 1450",
        "strength": "Standard Unit",
        "form": "Tablet",
        "manufacturer": "ePillID Dataset Sample",
        "description": "Reference laboratory photograph of pharmaceutical pill."
    },
    "310": {
        "class_name": "Pill_Ref_310",
        "generic_name": "Pharmaceutical Reference Sample 310",
        "strength": "Standard Unit",
        "form": "Tablet",
        "manufacturer": "ePillID Dataset Sample",
        "description": "Reference laboratory photograph of pharmaceutical pill."
    },
    "394": {
        "class_name": "Pill_Ref_394",
        "generic_name": "Pharmaceutical Reference Sample 394",
        "strength": "Standard Unit",
        "form": "Tablet",
        "manufacturer": "ePillID Dataset Sample",
        "description": "Reference laboratory photograph of pharmaceutical pill."
    },
    "735": {
        "class_name": "Pill_Ref_735",
        "generic_name": "Pharmaceutical Reference Sample 735",
        "strength": "Standard Unit",
        "form": "Tablet",
        "manufacturer": "ePillID Dataset Sample",
        "description": "Reference laboratory photograph of pharmaceutical pill."
    },
    "00078-0521-15": {
        "class_name": "Starlix",
        "generic_name": "Nateglinide",
        "strength": "120 mg",
        "form": "Tablet",
        "manufacturer": "Novartis Pharmaceuticals",
        "description": "Red round film-coated tablet for type 2 diabetes management."
    },
    "00555-0513-02": {
        "class_name": "Warfarin",
        "generic_name": "Warfarin Sodium",
        "strength": "5 mg",
        "form": "Tablet",
        "manufacturer": "Barr Laboratories",
        "description": "Peach round scored anticoagulant blood-thinner tablet."
    },
    "00603-5771-21": {
        "class_name": "Prednisone",
        "generic_name": "Prednisone",
        "strength": "20 mg",
        "form": "Tablet",
        "manufacturer": "Par Pharmaceutical",
        "description": "Peach round scored corticosteroid tablet for inflammation."
    }
}


def compute_file_hash(filepath: Path) -> str:
    """Compute SHA-256 hash of image file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def match_pill_metadata(filename: str) -> Tuple[str, str, Dict]:
    """Extract NDC code and metadata from filename."""
    stem = Path(filename).stem
    for ndc, meta in NDC_METADATA.items():
        if ndc in stem:
            return ndc, meta["class_name"], meta
    # Default fallback
    clean_name = stem.replace("-", "_").replace(".", "_")
    return stem, clean_name, {"class_name": clean_name, "generic_name": clean_name}


def prepare_pill_dataset(
    raw_dataset_dir: Path,
    processed_output_dir: Path,
    seed: int = RANDOM_SEED
) -> Dict:
    """
    Process, structure, split, and verify the pill dataset.
    """
    print("=" * 80)
    print("STEP 2: PREPARING PILL DATASET")
    print("=" * 80)
    print(f"Source: {raw_dataset_dir}")
    print(f"Destination: {processed_output_dir}")
    print(f"Random Seed: {seed}")

    raw_images = sorted(list(raw_dataset_dir.rglob("*.jpg")) + list(raw_dataset_dir.rglob("*.png")))
    total_found = len(raw_images)
    print(f"Total raw images discovered: {total_found}")

    if total_found == 0:
        raise FileNotFoundError(f"No pill images found in {raw_dataset_dir}")

    # Build inventory
    inventory = []
    hashes = set()
    for img_path in raw_images:
        fhash = compute_file_hash(img_path)
        if fhash in hashes:
            print(f"Warning: Exact duplicate hash detected for {img_path.name}")
        hashes.add(fhash)
        ndc, cls_name, meta = match_pill_metadata(img_path.name)
        inventory.append({
            "src_path": img_path,
            "filename": img_path.name,
            "hash": fhash,
            "ndc": ndc,
            "class_name": cls_name,
            "metadata": meta
        })

    # Unique classes
    unique_classes = sorted(list(set(item["class_name"] for item in inventory)))
    num_classes = len(unique_classes)
    class_to_idx = {cls_name: i for i, cls_name in enumerate(unique_classes)}
    idx_to_class = {i: cls_name for i, cls_name in enumerate(unique_classes)}

    print(f"Unique pill classes: {num_classes}")

    # Reproducible Split (60% Train, 20% Val, 20% Test)
    rng = np.random.RandomState(seed)
    indices = np.arange(total_found)
    rng.shuffle(indices)

    # For 20 images: 12 Train (60%), 4 Val (20%), 4 Test (20%)
    n_train = int(total_found * 0.60)
    n_val = int(total_found * 0.20)
    n_test = total_found - n_train - n_val

    train_indices = indices[:n_train]
    val_indices = indices[n_train:n_train + n_val]
    test_indices = indices[n_train + n_val:]

    train_items = [inventory[i] for i in train_indices]
    val_items = [inventory[i] for i in val_indices]
    test_items = [inventory[i] for i in test_indices]

    # Verify zero leakage across splits
    train_hashes = set(item["hash"] for item in train_items)
    val_hashes = set(item["hash"] for item in val_items)
    test_hashes = set(item["hash"] for item in test_items)

    leakage_train_val = train_hashes.intersection(val_hashes)
    leakage_train_test = train_hashes.intersection(test_hashes)
    leakage_val_test = val_hashes.intersection(test_hashes)

    if leakage_train_val or leakage_train_test or leakage_val_test:
        raise RuntimeError("DATA LEAKAGE DETECTED across splits! Aborting dataset preparation.")

    print("\n[LEAKAGE CHECK] PASSED: 0 file/hash overlap between Train, Val, and Test.")

    # Populate destination folders
    if processed_output_dir.exists():
        shutil.rmtree(processed_output_dir)

    for split_name, items in [("train", train_items), ("val", val_items), ("test", test_items)]:
        for item in items:
            cls_dir = processed_output_dir / split_name / item["class_name"]
            cls_dir.mkdir(parents=True, exist_ok=True)
            dst_file = cls_dir / item["filename"]
            shutil.copy2(item["src_path"], dst_file)

    # Save split metadata report
    split_info = {
        "random_seed": seed,
        "total_images": total_found,
        "num_classes": num_classes,
        "classes": unique_classes,
        "class_to_idx": class_to_idx,
        "idx_to_class": idx_to_class,
        "ndc_metadata": NDC_METADATA,
        "splits": {
            "train": {
                "count": len(train_items),
                "images": [item["filename"] for item in train_items],
                "classes": sorted(list(set(item["class_name"] for item in train_items)))
            },
            "val": {
                "count": len(val_items),
                "images": [item["filename"] for item in val_items],
                "classes": sorted(list(set(item["class_name"] for item in val_items)))
            },
            "test": {
                "count": len(test_items),
                "images": [item["filename"] for item in test_items],
                "classes": sorted(list(set(item["class_name"] for item in test_items)))
            }
        },
        "leakage_detected": False
    }

    info_path = processed_output_dir / "split_info.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(split_info, f, indent=2)

    print("\nDataset Preparation Complete:")
    print(f"  Train samples: {len(train_items)}")
    print(f"  Val samples:   {len(val_items)}")
    print(f"  Test samples:  {len(test_items)}")
    print(f"  Split info:    {info_path}")
    print("=" * 80)

    return split_info


if __name__ == "__main__":
    raw_dir = Path(r"C:\Users\Harshu\Desktop\Medicine\datasets\small_dataset_20_images")
    out_dir = Path(r"C:\Users\Harshu\Desktop\Medicine\pill_training\data\processed")
    prepare_pill_dataset(raw_dir, out_dir)
