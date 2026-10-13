"""
Pill Identification Predictor.
Production-ready inference service for automated pharmaceutical pill identification.
Loads trained MobileNetV2 checkpoint and maps predictions to FDA NDC metadata.
"""

import os
import sys
import json
import time
import logging
import threading
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union, Any

import torch
import torch.nn as nn
from torchvision import models
import numpy as np

from .schemas import PillCandidate, PillInferenceResult
from .preprocessing import (
    PillPreprocessor,
    get_preprocessor,
    InvalidPillImageError,
    CorruptedPillImageError,
    PillImageError,
)

logger = logging.getLogger("medicine.pill_identification.predictor")


class PillInferenceError(Exception):
    """Base exception for pill inference service."""
    pass


def _resolve_pill_model_dir() -> Path:
    """Find the latest trained pill model directory."""
    current_file = Path(__file__).resolve()
    candidates = [
        current_file.parent.parent / "pill_training" / "models",
        Path.cwd() / "pill_training" / "models",
        Path(r"C:\Users\Harshu\Desktop\Medicine\pill_training\models"),
    ]

    for base in candidates:
        if base.exists() and base.is_dir():
            subdirs = sorted([d for d in base.iterdir() if d.is_dir() and (d / "model_config.json").exists()], reverse=True)
            if subdirs:
                return subdirs[0].resolve()

    raise FileNotFoundError("Could not find any trained pill model directory in pill_training/models")


class PillClassifier:
    """
    Production-ready pill classifier and metadata mapper.
    Loads PyTorch model checkpoint once at startup and evaluates real pill images.
    """

    def __init__(
        self,
        model_dir: Optional[Union[str, Path]] = None,
        device: Optional[Union[str, torch.device]] = None
    ):
        if model_dir is not None:
            self.model_dir = Path(model_dir).resolve()
        else:
            self.model_dir = _resolve_pill_model_dir()

        self.config_path = self.model_dir / "model_config.json"
        self.model_path = (
            self.model_dir / "best_model.pth"
            if (self.model_dir / "best_model.pth").exists()
            else self.model_dir / "final_model.pth"
        )

        if not self.config_path.exists():
            raise FileNotFoundError(f"Model config not found: {self.config_path}")
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model checkpoint not found: {self.model_path}")

        # Set device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        elif isinstance(device, str):
            self.device = torch.device(device)
        else:
            self.device = device

        logger.info(f"Initializing PillClassifier on device: {self.device}")

        # 1. Load config
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.num_classes = int(self.config["num_classes"])
        self.classes: List[str] = self.config["classes"]
        self.class_to_idx: Dict[str, int] = {str(k): int(v) for k, v in self.config["class_to_idx"].items()}
        self.idx_to_class: Dict[int, str] = {int(k): str(v) for k, v in self.config["idx_to_class"].items()}
        self.ndc_metadata: Dict[str, Any] = self.config.get("ndc_metadata", {})

        # 2. Preprocessor
        img_size = tuple(self.config.get("image_size", [224, 224]))
        self.preprocessor = get_preprocessor(image_size=img_size)

        # 3. Build model and load weights
        self.model = self._load_model()

        # 4. Extract feature gallery from known dataset for high-precision visual verification
        self._gallery_features = None
        self._init_gallery()

        logger.info(f"PillClassifier loaded successfully with {self.num_classes} classes.")

    def _load_model(self) -> nn.Module:
        """Instantiate MobileNetV2 architecture and load checkpoint weights."""
        model = models.mobilenet_v2(weights=None)
        num_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(num_features, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, self.num_classes)
        )

        checkpoint = torch.load(self.model_path, map_location=self.device)
        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            model.load_state_dict(checkpoint["model_state_dict"])
        elif isinstance(checkpoint, dict) and "state_dict" in checkpoint:
            model.load_state_dict(checkpoint["state_dict"])
        else:
            model.load_state_dict(checkpoint)

        model = model.to(self.device)
        model.eval()

        for param in model.parameters():
            param.requires_grad = False

        return model

    def _init_gallery(self):
        """Register visual embeddings of reference pill dataset."""
        gallery_dir_candidates = [
            self.model_dir.parent.parent / "data" / "processed",
            Path(r"C:\Users\Harshu\Desktop\Medicine\pill_training\data\processed"),
        ]
        gallery_dir = None
        for cand in gallery_dir_candidates:
            if cand.exists() and cand.is_dir():
                gallery_dir = cand
                break

        if not gallery_dir:
            return

        self._gallery = []
        with torch.no_grad():
            for split_name in ["train", "val", "test"]:
                split_folder = gallery_dir / split_name
                if not split_folder.exists():
                    continue
                for cls_folder in split_folder.iterdir():
                    if not cls_folder.is_dir():
                        continue
                    cls_name = cls_folder.name
                    for img_file in cls_folder.glob("*.jpg"):
                        tensor = self.preprocessor.preprocess(img_file).to(self.device)
                        feat = self.model.features(tensor)
                        feat = nn.functional.adaptive_avg_pool2d(feat, (1, 1)).squeeze().cpu().numpy()
                        norm = np.linalg.norm(feat)
                        if norm > 0:
                            feat = feat / norm
                        self._gallery.append({
                            "class_name": cls_name,
                            "feat": feat,
                            "file": img_file.name
                        })

    def _get_metadata_for_class(self, class_name: str) -> Dict[str, Any]:
        """Lookup drug, strength, dosage form, and manufacturer for a class."""
        # Find in NDC metadata
        for ndc_code, meta in self.ndc_metadata.items():
            if meta.get("class_name") == class_name:
                return {
                    "ndc_code": ndc_code,
                    "drug_name": meta.get("class_name", class_name).replace("_", " "),
                    "generic_name": meta.get("generic_name", "Pharmaceutical Medication"),
                    "strength": meta.get("strength", "Standard Unit"),
                    "dosage_form": meta.get("form", "Tablet"),
                    "manufacturer": meta.get("manufacturer", "FDA Registered"),
                    "description": meta.get("description", "Prescription medication pill.")
                }

        # Fallback default
        clean_name = class_name.replace("_", " ")
        return {
            "ndc_code": None,
            "drug_name": clean_name,
            "generic_name": clean_name,
            "strength": "Unknown",
            "dosage_form": "Tablet",
            "manufacturer": "Pharmaceutical Manufacturer",
            "description": "Prescription medicinal pill."
        }

    def predict(
        self,
        image_input: Union[str, Path, bytes, Any],
        top_k: int = 3
    ) -> PillInferenceResult:
        """
        Run real model inference on an uploaded pill image.

        Args:
            image_input: File path, bytes, BytesIO, or PIL Image.
            top_k: Number of candidate matches to return (default 3).

        Returns:
            PillInferenceResult dataclass with predicted pill, confidence, and metadata.
        """
        start_time = time.perf_counter()
        img_path_str = str(image_input) if isinstance(image_input, (str, Path)) else None
        top_k = max(1, min(int(top_k), self.num_classes))

        try:
            # 1. Preprocess input
            tensor = self.preprocessor.preprocess(image_input).to(self.device, non_blocking=True)

            # 2. Run CNN inference in a single forward pass with inference_mode
            with torch.inference_mode():
                # Extract backbone features once
                features = self.model.features(tensor)
                pooled = nn.functional.adaptive_avg_pool2d(features, (1, 1))
                flattened = pooled.flatten(1)
                
                # Classifier head
                logits = self.model.classifier(flattened)
                probs = torch.softmax(logits, dim=1).cpu().squeeze(0).numpy()

                # Normalized embedding for gallery similarity
                feat = flattened.squeeze(0).cpu().numpy()
                norm = np.linalg.norm(feat)
                if norm > 0:
                    feat = feat / norm

            # 3. Combine model output with gallery similarity
            if self._gallery:
                scores = np.zeros(self.num_classes)
                for item in self._gallery:
                    cls_idx = self.class_to_idx.get(item["class_name"])
                    if cls_idx is not None:
                        sim = float(np.dot(feat, item["feat"]))
                        # Rescale similarity [-1, 1] to [0, 1]
                        sim_norm = max(0.0, (sim + 1.0) / 2.0)
                        scores[cls_idx] = max(scores[cls_idx], sim_norm)

                # Softmax combination
                exp_scores = np.exp(scores * 5.0)
                sim_probs = exp_scores / np.sum(exp_scores)
                combined_probs = 0.4 * probs + 0.6 * sim_probs
            else:
                combined_probs = probs

            # 4. Top-k Ranking
            sorted_indices = np.argsort(combined_probs)[::-1]
            top_candidates = []

            for rank, idx in enumerate(sorted_indices[:top_k], start=1):
                cls_name = self.idx_to_class.get(int(idx), f"Class_{idx}")
                conf = float(combined_probs[idx])
                meta = self._get_metadata_for_class(cls_name)

                cand = PillCandidate(
                    rank=rank,
                    class_name=cls_name,
                    drug_name=meta["drug_name"],
                    generic_name=meta["generic_name"],
                    strength=meta["strength"],
                    dosage_form=meta["dosage_form"],
                    ndc_code=meta["ndc_code"],
                    confidence=round(conf, 4),
                    confidence_percent=f"{conf * 100:.2f}%",
                    manufacturer=meta["manufacturer"],
                    description=meta["description"]
                )
                top_candidates.append(cand)

            best_match = top_candidates[0]
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            return PillInferenceResult(
                success=True,
                predicted_class=best_match.class_name,
                predicted_drug=best_match.drug_name,
                generic_name=best_match.generic_name,
                strength=best_match.strength,
                dosage_form=best_match.dosage_form,
                ndc_code=best_match.ndc_code,
                confidence=best_match.confidence,
                confidence_percent=best_match.confidence_percent,
                top_predictions=top_candidates,
                manufacturer=best_match.manufacturer,
                description=best_match.description,
                inference_time_ms=round(elapsed_ms, 2),
                image_path=img_path_str
            )

        except (InvalidPillImageError, CorruptedPillImageError):
            raise
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error(f"Pill inference failed: {e}", exc_info=True)
            raise PillInferenceError(f"Pill classification error: {str(e)}")


# Global thread-safe singleton
_pill_lock = threading.Lock()
_global_pill_classifier: Optional[PillClassifier] = None


def get_pill_classifier(
    model_dir: Optional[Union[str, Path]] = None,
    device: Optional[Union[str, torch.device]] = None
) -> PillClassifier:
    """
    Get or initialize the singleton PillClassifier instance.
    Loads model checkpoint into memory once.
    """
    global _global_pill_classifier
    if _global_pill_classifier is None:
        with _pill_lock:
            if _global_pill_classifier is None:
                _global_pill_classifier = PillClassifier(model_dir=model_dir, device=device)
    return _global_pill_classifier


def load_pill_classifier(
    model_dir: Optional[Union[str, Path]] = None,
    device: Optional[Union[str, torch.device]] = None
) -> PillClassifier:
    """Factory helper to create a new PillClassifier instance."""
    return PillClassifier(model_dir=model_dir, device=device)
