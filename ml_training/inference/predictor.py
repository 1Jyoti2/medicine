"""
Model predictor for medicinal leaf classification.
Production-ready, reusable inference service designed for FastAPI backend and CLI scripts.
"""

import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import torch
import torch.nn as nn
from torchvision import models
import numpy as np

from .preprocessing import (
    ImagePreprocessor,
    ImageProcessingError,
    InvalidImageError,
    CorruptedImageError,
    ImageDimensionError,
)

logger = logging.getLogger("medicine.inference.predictor")


class LeafInferenceError(Exception):
    """Base exception for leaf inference service."""
    pass


class ModelLoadError(LeafInferenceError):
    """Raised when model weights or architecture failed to load."""
    pass


class ModelConfigError(LeafInferenceError):
    """Raised when model configuration is missing or invalid."""
    pass


class PredictionError(LeafInferenceError):
    """Raised when inference execution fails on input data."""
    pass


# Default trained model directory relative to repo/package
DEFAULT_MODEL_DIR_NAME = "training_20260919_135002"


def _resolve_default_model_dir() -> Path:
    """Find default model directory across standard relative locations."""
    current_file = Path(__file__).resolve()
    ml_training_dir = current_file.parent.parent  # ml_training/

    candidate_paths = [
        ml_training_dir / "models" / DEFAULT_MODEL_DIR_NAME,
        Path.cwd() / "ml_training" / "models" / DEFAULT_MODEL_DIR_NAME,
        Path.cwd() / "models" / DEFAULT_MODEL_DIR_NAME,
        Path(r"C:\Users\Harshu\Desktop\Medicine\ml_training\models\training_20260919_135002"),
    ]

    for path in candidate_paths:
        if path.exists() and (path / "final_model.pth").exists() and (path / "model_config.json").exists():
            return path.resolve()

    return (ml_training_dir / "models" / DEFAULT_MODEL_DIR_NAME).resolve()


def _resolve_metadata_file() -> Optional[Path]:
    """Find medicinal plants metadata JSON if available."""
    current_file = Path(__file__).resolve()
    ml_training_dir = current_file.parent.parent

    candidate_paths = [
        ml_training_dir / "data" / "medicinal_plants_metadata.json",
        Path.cwd() / "ml_training" / "data" / "medicinal_plants_metadata.json",
        Path(r"C:\Users\Harshu\Desktop\Medicine\ml_training\data\medicinal_plants_metadata.json"),
    ]

    for path in candidate_paths:
        if path.exists() and path.is_file():
            return path.resolve()
    return None


class LeafClassifier:
    """
    Production-ready leaf classification predictor.
    Loads PyTorch model checkpoint and configuration once,
    provides fast inference for single and batch images.
    """

    def __init__(
        self,
        model_dir: Optional[Union[str, Path]] = None,
        model_path: Optional[Union[str, Path]] = None,
        config_path: Optional[Union[str, Path]] = None,
        device: Optional[Union[str, torch.device]] = None,
    ):
        """
        Initialize the LeafClassifier.

        Args:
            model_dir: Path to model folder containing 'final_model.pth' and 'model_config.json'
            model_path: Explicit path to model checkpoint (.pth)
            config_path: Explicit path to configuration file (.json)
            device: 'cuda', 'cpu', or torch.device. If None, auto-detected.
        """
        if model_dir is not None:
            base_dir = Path(model_dir).resolve()
            self.model_path = base_dir / "final_model.pth"
            self.config_path = base_dir / "model_config.json"
        elif model_path is not None and config_path is not None:
            self.model_path = Path(model_path).resolve()
            self.config_path = Path(config_path).resolve()
        else:
            default_dir = _resolve_default_model_dir()
            self.model_path = default_dir / "final_model.pth"
            self.config_path = default_dir / "model_config.json"

        if not self.model_path.exists():
            raise ModelLoadError(f"Trained model weights file not found: {self.model_path}")
        if not self.config_path.exists():
            raise ModelConfigError(f"Model configuration file not found: {self.config_path}")

        # Configure hardware device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        elif isinstance(device, str):
            self.device = torch.device(device)
        else:
            self.device = device

        logger.info(f"Initializing LeafClassifier on device: {self.device}")

        # 1. Load configuration and class mappings
        self.config = self._load_and_validate_config()
        self.num_classes = int(self.config["num_classes"])
        self.classes: List[str] = self.config["classes"]
        self.class_to_idx: Dict[str, int] = {str(k): int(v) for k, v in self.config["class_to_idx"].items()}
        self.idx_to_class: Dict[int, str] = {int(k): str(v) for k, v in self.config["idx_to_class"].items()}

        # 2. Preprocessor initialization
        image_size = tuple(self.config.get("image_size", [224, 224]))
        self.preprocessor = ImagePreprocessor(image_size=image_size)

        # 3. Load plant metadata database if available
        self.plants_metadata = self._load_plants_metadata()

        # 4. Load OOD Class Centroids for leaf vs non-leaf validation
        self.ood_centroids = self._load_ood_centroids()

        # 5. Build architecture and load model weights
        self.model = self._build_and_load_model()

        logger.info(
            f"LeafClassifier successfully loaded model '{self.config.get('model_type', 'mobilenet_v2')}' "
            f"with {self.num_classes} classes from path: {self.model_path}"
        )

    def _load_and_validate_config(self) -> Dict[str, Any]:
        """Read and validate model_config.json structure."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            required_keys = ["model_type", "num_classes", "classes", "idx_to_class", "image_size"]
            missing = [k for k in required_keys if k not in config]
            if missing:
                raise ModelConfigError(f"Missing required keys in model config: {missing}")

            return config
        except Exception as e:
            if isinstance(e, LeafInferenceError):
                raise
            raise ModelConfigError(f"Failed to parse model configuration at {self.config_path}: {str(e)}")

    def _load_plants_metadata(self) -> Dict[str, Any]:
        """Load medicinal plant descriptions and traditional use metadata."""
        meta_file = _resolve_metadata_file()
        if meta_file and meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load plant metadata file ({meta_file}): {e}")
        return {}

    def _load_ood_centroids(self) -> Dict[str, Any]:
        """Load calibrated class centroids for Out-Of-Distribution and leaf verification."""
        centroids_file = self.model_path.parent / "leaf_ood_centroids.json"
        if centroids_file.exists():
            try:
                with open(centroids_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info("Loaded leaf OOD centroids for non-leaf verification.")
                return data
            except Exception as e:
                logger.warning(f"Failed to load OOD centroids ({centroids_file}): {e}")
        return {}

    def _build_and_load_model(self) -> nn.Module:
        """Instantiate network architecture and load checkpoint weights."""
        model_type = self.config.get("model_type", "mobilenet_v2").lower()

        try:
            if model_type == "mobilenet_v2":
                base_model = models.mobilenet_v2(weights=None)
                num_features = base_model.classifier[1].in_features
                base_model.classifier = nn.Sequential(
                    nn.Dropout(0.5),
                    nn.Linear(num_features, 256),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(256, 128),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(128, self.num_classes),
                )
                model = base_model

            elif model_type == "resnet50":
                base_model = models.resnet50(weights=None)
                num_features = base_model.fc.in_features
                base_model.fc = nn.Sequential(
                    nn.Dropout(0.5),
                    nn.Linear(num_features, 512),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(512, 256),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(256, self.num_classes),
                )
                model = base_model

            elif model_type == "efficientnet_b0":
                base_model = models.efficientnet_b0(weights=None)
                num_features = base_model.classifier[1].in_features
                base_model.classifier = nn.Sequential(
                    nn.Dropout(0.5),
                    nn.Linear(num_features, 256),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(256, 128),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(128, self.num_classes),
                )
                model = base_model
            else:
                raise ModelLoadError(f"Unsupported model type in config: '{model_type}'")

            # Load checkpoint
            checkpoint = torch.load(self.model_path, map_location=self.device)
            if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                model.load_state_dict(checkpoint["model_state_dict"])
            elif isinstance(checkpoint, dict) and "state_dict" in checkpoint:
                model.load_state_dict(checkpoint["state_dict"])
            else:
                model.load_state_dict(checkpoint)

            model = model.to(self.device)
            model.eval()

            # Disable gradients on all parameters for inference safety
            for param in model.parameters():
                param.requires_grad = False

            return model

        except Exception as e:
            if isinstance(e, LeafInferenceError):
                raise
            raise ModelLoadError(f"Failed to build or load model weights from {self.model_path}: {str(e)}")

    def predict(
        self,
        image_input: Union[str, Path, bytes, Any],
        top_k: int = 3,
        include_metadata: bool = True,
    ) -> Dict[str, Any]:
        """
        Run real model inference on a single image input with multi-signal OOD leaf verification.
        """
        top_k = max(1, min(int(top_k), self.num_classes))
        start_time = time.perf_counter()

        try:
            # 1. Load and validate PIL Image for domain / color analysis
            pil_img = self.preprocessor.load_and_validate_pil(image_input)
            img_w, img_h = pil_img.size

            # Compute botanical color & vegetation features
            img_np = np.array(pil_img, dtype=np.float32)
            r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]
            total = r + g + b + 1e-6
            exg = (2.0 * g - r - b) / total
            exg_pos_ratio = float(np.mean(exg > 0.02))

            img_hsv = pil_img.convert("HSV")
            hsv_np = np.array(img_hsv, dtype=np.float32)
            h = hsv_np[:, :, 0] * (360.0 / 255.0)
            s = hsv_np[:, :, 1] / 255.0
            v = hsv_np[:, :, 2] / 255.0
            green_ratio = float(np.mean((h >= 30) & (h <= 175) & (s >= 0.10) & (v >= 0.10)))

            # Skin tone detection in YCbCr space
            img_ycbcr = pil_img.convert("YCbCr")
            ycbcr_np = np.array(img_ycbcr, dtype=np.uint8)
            cb = ycbcr_np[:, :, 1]
            cr = ycbcr_np[:, :, 2]
            skin_mask = (cr >= 133) & (cr <= 173) & (cb >= 77) & (cb <= 127)
            skin_ratio = float(np.mean(skin_mask))

            # 2. Preprocess input tensor
            tensor = self.preprocessor.preprocess(pil_img)
            tensor = tensor.to(self.device, non_blocking=True)

            # 3. Extract deep feature embeddings and logits
            with torch.inference_mode():
                feat = self.model.features(tensor)
                feat = torch.nn.functional.adaptive_avg_pool2d(feat, (1, 1)).flatten(1)
                logits = self.model.classifier(feat)
                probs_tensor = torch.softmax(logits, dim=1)

            probs = probs_tensor.cpu().squeeze(0).tolist()
            feat_vec = feat.cpu().numpy().squeeze()
            feat_norm = feat_vec / (np.linalg.norm(feat_vec) + 1e-8)

            # 4. Compute cosine similarity with calibrated leaf centroids
            max_cos_sim = 0.0
            cos_sims = {}
            if self.ood_centroids and "class_centroids" in self.ood_centroids:
                for cls_name, c_vec in self.ood_centroids["class_centroids"].items():
                    c_arr = np.array(c_vec, dtype=np.float32)
                    sim = float(np.dot(feat_norm, c_arr))
                    cos_sims[cls_name] = sim
                max_cos_sim = max(cos_sims.values()) if cos_sims else 0.0

            # 5. Build all probabilities map
            all_probabilities = {
                self.idx_to_class[i]: float(probs[i])
                for i in range(len(probs))
            }

            # Log complete probability distribution safely
            dist_str = ", ".join([f"{k}: {v*100:.2f}%" for k, v in all_probabilities.items()])
            logger.info(f"Model Softmax Distribution: [{dist_str}]")

            # 6. Multi-Signal Leaf vs Non-Leaf (OOD) Decision Strategy
            is_leaf = True
            rejection_reason = None

            if self.ood_centroids:
                sim_threshold = float(self.ood_centroids.get("similarity_threshold", 0.46))

                # Rule 1: Deep feature manifold boundary test
                if max_cos_sim < sim_threshold:
                    is_leaf = False
                    rejection_reason = f"Out-of-distribution image (similarity {max_cos_sim:.3f} < {sim_threshold})"
                # Rule 2: Human selfie/face detection
                elif skin_ratio > 0.35 and green_ratio < 0.02 and exg_pos_ratio < 0.02:
                    is_leaf = False
                    rejection_reason = "Human face/selfie detected instead of a medicinal leaf"
                # Rule 3: Absence of vegetation features with borderline similarity
                elif green_ratio < 0.003 and exg_pos_ratio < 0.008 and max_cos_sim < 0.60:
                    is_leaf = False
                    rejection_reason = "Non-botanical object detected"

            # Sort indices by highest probability
            sorted_indices = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)
            predicted_idx = sorted_indices[0]
            raw_predicted_class = self.idx_to_class.get(predicted_idx, f"Class_{predicted_idx}")
            raw_confidence = float(probs[predicted_idx])

            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            if not is_leaf:
                logger.warning(
                    f"Non-leaf image rejected: {rejection_reason} "
                    f"(Raw Softmax: {raw_predicted_class} {raw_confidence*100:.1f}%, "
                    f"MaxSim: {max_cos_sim:.3f}, Green: {green_ratio*100:.1f}%, Skin: {skin_ratio*100:.1f}%)"
                )
                return {
                    "success": False,
                    "is_leaf": False,
                    "predicted_class": None,
                    "confidence": 0.0,
                    "confidence_percent": "0.00%",
                    "top_predictions": [],
                    "all_probabilities": all_probabilities,
                    "rejection_reason": rejection_reason,
                    "message": "Please upload a clear medicinal leaf image. The uploaded image does not appear to contain a valid medicinal leaf.",
                    "inference_time_ms": round(elapsed_ms, 2),
                    "debug_info": {
                        "received_dimensions": f"{img_w}x{img_h}",
                        "model_name": self.config.get("model_type", "mobilenet_v2"),
                        "model_path": str(self.model_path),
                        "max_cosine_similarity": round(float(max_cos_sim), 4),
                        "green_ratio": round(float(green_ratio), 4),
                        "skin_ratio": round(float(skin_ratio), 4),
                    },
                }

            # 7. Build top-k predictions list for authentic leaves
            top_predictions = []
            for rank, idx in enumerate(sorted_indices[:top_k], start=1):
                cls_name = self.idx_to_class.get(idx, f"Class_{idx}")
                prob = float(probs[idx])
                entry = {
                    "rank": rank,
                    "class": cls_name,
                    "confidence": prob,
                    "confidence_percent": f"{prob * 100:.2f}%",
                }
                if cls_name in self.plants_metadata:
                    meta = self.plants_metadata[cls_name]
                    entry["scientific_name"] = meta.get("scientificName", cls_name)
                    entry["common_names"] = meta.get("commonNames", [])
                top_predictions.append(entry)

            result = {
                "success": True,
                "is_leaf": True,
                "predicted_class": raw_predicted_class,
                "confidence": raw_confidence,
                "confidence_percent": f"{raw_confidence * 100:.2f}%",
                "top_predictions": top_predictions,
                "all_probabilities": all_probabilities,
                "inference_time_ms": round(elapsed_ms, 2),
                "debug_info": {
                    "received_dimensions": f"{img_w}x{img_h}",
                    "model_name": self.config.get("model_type", "mobilenet_v2"),
                    "model_path": str(self.model_path),
                    "max_cosine_similarity": round(float(max_cos_sim), 4),
                    "green_ratio": round(float(green_ratio), 4),
                    "skin_ratio": round(float(skin_ratio), 4),
                },
            }

            if include_metadata and raw_predicted_class in self.plants_metadata:
                result["plant_metadata"] = self.plants_metadata[raw_predicted_class]

            logger.info(
                f"Leaf Prediction successful: {raw_predicted_class} ({raw_confidence * 100:.2f}%) "
                f"in {elapsed_ms:.1f}ms [MaxSim: {max_cos_sim:.3f}]"
            )
            return result

        except (ImageProcessingError, InvalidImageError, CorruptedImageError, ImageDimensionError) as e:
            logger.warning(f"Image validation/preprocessing failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Inference execution failed: {e}", exc_info=True)
            raise PredictionError(f"Model prediction failed: {str(e)}")

    def predict_batch(
        self,
        image_inputs: List[Union[str, Path, bytes, Any]],
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Run inference across a batch of images. Handles individual failures gracefully.
        """
        results = []
        for item in image_inputs:
            item_id = str(item) if isinstance(item, (str, Path)) else f"image_{len(results)}"
            try:
                res = self.predict(item, top_k=top_k, include_metadata=False)
                res["input_identifier"] = item_id
                results.append(res)
            except Exception as e:
                results.append({
                    "success": False,
                    "input_identifier": item_id,
                    "error": str(e),
                    "error_type": e.__class__.__name__,
                })
        return results

    def get_model_info(self) -> Dict[str, Any]:
        """Return model metadata, architecture details, and supported classes."""
        return {
            "model_type": self.config.get("model_type", "mobilenet_v2"),
            "num_classes": self.num_classes,
            "classes": self.classes,
            "image_size": self.config.get("image_size", [224, 224]),
            "device": str(self.device),
            "model_path": str(self.model_path),
            "config_path": str(self.config_path),
            "best_val_accuracy": self.config.get("best_val_accuracy"),
            "training_date": self.config.get("training_date"),
        }


# Global singleton cache protected with a mutex lock
_singleton_lock = threading.Lock()
_global_classifier: Optional[LeafClassifier] = None


def load_classifier(
    model_dir: Optional[Union[str, Path]] = None,
    device: Optional[Union[str, torch.device]] = None,
) -> LeafClassifier:
    """
    Factory function to create a new instance of LeafClassifier.
    """
    return LeafClassifier(model_dir=model_dir, device=device)


def get_classifier(
    model_dir: Optional[Union[str, Path]] = None,
    device: Optional[Union[str, torch.device]] = None,
) -> LeafClassifier:
    """
    Get or create the singleton instance of LeafClassifier.
    Guarantees the model is loaded into memory only once across the application lifecycle.
    """
    global _global_classifier

    if _global_classifier is None:
        with _singleton_lock:
            if _global_classifier is None:
                _global_classifier = LeafClassifier(model_dir=model_dir, device=device)

    return _global_classifier
