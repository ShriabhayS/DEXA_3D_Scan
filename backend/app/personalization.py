"""
Body (and optional face) personalization utilities.
"""
from __future__ import annotations

import contextlib
from pathlib import Path
from typing import Dict, Optional

import cv2
import numpy as np

from .models import DexaScanData

try:
    import mediapipe as mp

    _POSE = mp.solutions.pose.Pose(static_image_mode=True)
    _FACE_MESH = mp.solutions.face_mesh.FaceMesh(static_image_mode=True)
except Exception:  # pragma: no cover - mediapipe may be unavailable in CI
    _POSE = None
    _FACE_MESH = None


def _load_image(image_path: Path) -> np.ndarray:
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Failed to load image: {image_path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def _compute_distance(a, b) -> float:
    return float(np.linalg.norm(np.array(a) - np.array(b)))


def extract_body_measurements(image_path: Path) -> Dict[str, float]:
    """
    Use MediaPipe Pose (if available) to derive body width / limb ratios.
    If MediaPipe is unavailable, returns an empty dict so the pipeline
    can continue without personalization.
    """

    if _POSE is None:
        return {}

    image = _load_image(image_path)
    results = _POSE.process(image)
    if not results.pose_landmarks:
        return {}

    landmarks = results.pose_landmarks.landmark
    def _pt(index: int) -> np.ndarray:
        lm = landmarks[index]
        return np.array([lm.x, lm.y])

    shoulders = _compute_distance(_pt(11), _pt(12))
    hips = _compute_distance(_pt(23), _pt(24))
    chest = _compute_distance(_pt(11), _pt(23))

    return {
        "shoulder_width": shoulders,
        "hip_width": hips,
        "torso_length": chest,
    }


def derive_scale_adjustments(
    measurements: Dict[str, float], dexa_data: DexaScanData
) -> Dict[str, float]:
    """
    Convert raw photo measurements into scale overrides used by the
    avatar generator. Values close to 1.0 indicate no change.
    """

    if not measurements:
        return {}

    scales = {}
    shoulder_ratio = measurements.get("shoulder_width")
    hip_ratio = measurements.get("hip_width")

    if shoulder_ratio:
        scales["shoulders"] = 1.0 + (shoulder_ratio - 0.3)
    if hip_ratio:
        scales["hips"] = 1.0 + (hip_ratio - 0.3)

    if dexa_data.body_metrics.total_fat_percent:
        fat = dexa_data.body_metrics.total_fat_percent
        scales["waist"] = 1.0 + (fat - 25.0) / 100.0

    return scales


def refine_parameters_with_photo(
    dexa_data: DexaScanData, photo_path: Optional[Path]
) -> Dict[str, float]:
    """
    Entry point used by the FastAPI backend. Handles failures gracefully
    so avatar generation still succeeds when personalization assets are
    missing or invalid.
    """

    if not photo_path:
        return {}

    with contextlib.suppress(Exception):
        measurements = extract_body_measurements(photo_path)
        return derive_scale_adjustments(measurements, dexa_data)

    return {}


