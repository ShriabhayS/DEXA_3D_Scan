"""
DEXA metric → SMPL-X parameter conversion utilities.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from uuid import uuid4

import numpy as np
import trimesh
from trimesh.creation import icosphere

from .models import AvatarGenerationResponse, AvatarParameters, DexaScanData


SMPLX_MODEL_DIR = Path(os.getenv("SMPLX_MODEL_DIR", Path("models")))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", Path("output")))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _normalize(value: Optional[float], reference: float) -> float:
    if value is None:
        return 0.0
    return float(value) / reference


def map_metrics_to_parameters(dexa_data: DexaScanData, body_scale_adjustments: Optional[Dict[str, float]] = None) -> AvatarParameters:
    """Translate DEXA metrics into simplified SMPL-X parameter space."""

    body = dexa_data.body_metrics
    betas = np.zeros(10, dtype=np.float32)

    betas[0] = _normalize(body.total_fat_percent, 40.0)  # torso thickness
    betas[1] = _normalize(body.total_lean_mass_kg, 70.0)  # musculature
    betas[2] = _normalize(body.height_cm, 170.0)  # stature
    betas[3] = _normalize(body.weight_kg, 80.0)  # global scale

    if "android" in dexa_data.regions:
        betas[4] = _normalize(dexa_data.regions["android"].fat_percent, 40.0)
    if "gynoid" in dexa_data.regions:
        betas[5] = _normalize(dexa_data.regions["gynoid"].fat_percent, 45.0)

    scales = body_scale_adjustments or {}

    return AvatarParameters(
        betas=betas.tolist(),
        scales=scales,
        notes="Approximate parameters generated from DEXA metrics",
    )


def _create_placeholder_mesh(scale: float = 1.0) -> trimesh.Trimesh:
    mesh = icosphere(subdivisions=4, radius=scale)
    mesh.apply_scale([0.7, 1.2, 0.5])  # elongated to mimic a torso
    return mesh


def _export_glb(mesh: trimesh.Trimesh, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    scene = trimesh.Scene(mesh)
    scene.export(destination, file_type="glb")


def generate_avatar_assets(parameters: AvatarParameters) -> Tuple[str, str, str]:
    """
    Produce a GLB file (placeholder) and preview metadata for the given parameters.
    Returns tuple of (avatar_id, glb_path, metadata_path) as relative paths.
    """

    avatar_id = uuid4().hex
    glb_path = OUTPUT_DIR / f"{avatar_id}.glb"

    scale = 1.0 + float(parameters.betas[0]) * 0.1 if parameters.betas else 1.0
    mesh = _create_placeholder_mesh(scale)
    _export_glb(mesh, glb_path)

    metadata_path = OUTPUT_DIR / f"{avatar_id}.json"
    metadata_path.write_text(json.dumps(parameters.dict(), indent=2))

    # Return relative paths for API responses
    glb_relative = f"output/{avatar_id}.glb"
    metadata_relative = f"output/{avatar_id}.json"
    return avatar_id, glb_relative, metadata_relative


def process_dexa_to_avatar(
    dexa_data: DexaScanData,
    body_scale_adjustments: Optional[Dict[str, float]] = None,
) -> AvatarGenerationResponse:
    parameters = map_metrics_to_parameters(dexa_data, body_scale_adjustments)
    avatar_id, glb_path, metadata_path = generate_avatar_assets(parameters)
    return AvatarGenerationResponse(
        avatar_id=avatar_id,
        glb_path=glb_path,
        preview_image_path=None,
        parameters=parameters,
    )


