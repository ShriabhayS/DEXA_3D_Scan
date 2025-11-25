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
from .smplx_loader import generate_smplx_mesh


SMPLX_MODEL_DIR = Path(os.getenv("SMPLX_MODEL_DIR", Path("models")))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", Path("output")))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _normalize(value: Optional[float], reference: float) -> float:
    if value is None:
        return 0.0
    return float(value) / reference


def map_metrics_to_parameters(dexa_data: DexaScanData, body_scale_adjustments: Optional[Dict[str, float]] = None) -> AvatarParameters:
    """
    Translate DEXA metrics into SMPL-X parameter space.
    
    SMPL-X uses 10 shape parameters (betas) that control body shape:
    - beta[0]: Overall body shape (thin to heavy)
    - beta[1]: Height/stature
    - beta[2]: Muscle definition
    - beta[3-9]: Regional body shape variations
    
    We map DEXA metrics to these parameters based on body composition.
    """
    body = dexa_data.body_metrics
    betas = np.zeros(10, dtype=np.float32)

    # Beta 0: Overall body shape (based on body fat %)
    # Higher fat % = more rounded/heavier shape
    if body.total_fat_percent is not None:
        # Normalize to -2 to +2 range (SMPL-X typical range)
        fat_normalized = (body.total_fat_percent - 25.0) / 15.0  # Center at 25%, scale by 15%
        betas[0] = np.clip(fat_normalized, -2.0, 2.0)
    
    # Beta 1: Height/stature
    if body.height_cm is not None:
        # Normalize around 170cm (average)
        height_normalized = (body.height_cm - 170.0) / 20.0
        betas[1] = np.clip(height_normalized, -2.0, 2.0)
    
    # Beta 2: Muscle definition (based on lean mass)
    if body.total_lean_mass_kg is not None:
        # Higher lean mass = more muscular
        lean_normalized = (body.total_lean_mass_kg - 50.0) / 20.0
        betas[2] = np.clip(lean_normalized, -2.0, 2.0)
    
    # Beta 3: Weight/overall scale
    if body.weight_kg is not None:
        weight_normalized = (body.weight_kg - 70.0) / 20.0
        betas[3] = np.clip(weight_normalized, -2.0, 2.0)
    
    # Beta 4: Android fat distribution (waist/abdomen)
    if "android" in dexa_data.regions and dexa_data.regions["android"].fat_percent is not None:
        android_fat = dexa_data.regions["android"].fat_percent
        android_normalized = (android_fat - 30.0) / 15.0
        betas[4] = np.clip(android_normalized, -2.0, 2.0)
    
    # Beta 5: Gynoid fat distribution (hips/thighs)
    if "gynoid" in dexa_data.regions and dexa_data.regions["gynoid"].fat_percent is not None:
        gynoid_fat = dexa_data.regions["gynoid"].fat_percent
        gynoid_normalized = (gynoid_fat - 35.0) / 15.0
        betas[5] = np.clip(gynoid_normalized, -2.0, 2.0)
    
    # Beta 6-9: Regional adjustments based on arm/leg/trunk measurements
    if "arms" in dexa_data.regions and dexa_data.regions["arms"].fat_percent is not None:
        arm_fat = dexa_data.regions["arms"].fat_percent
        betas[6] = np.clip((arm_fat - 25.0) / 15.0, -2.0, 2.0)
    
    if "legs" in dexa_data.regions and dexa_data.regions["legs"].fat_percent is not None:
        leg_fat = dexa_data.regions["legs"].fat_percent
        betas[7] = np.clip((leg_fat - 30.0) / 15.0, -2.0, 2.0)
    
    if "trunk" in dexa_data.regions and dexa_data.regions["trunk"].fat_percent is not None:
        trunk_fat = dexa_data.regions["trunk"].fat_percent
        betas[8] = np.clip((trunk_fat - 30.0) / 15.0, -2.0, 2.0)
    
    # Beta 9: Overall body proportion (can be used for additional adjustments)
    if body.total_bone_mass_kg is not None:
        # Bone mass affects overall frame size
        bone_normalized = (body.total_bone_mass_kg - 3.0) / 1.5
        betas[9] = np.clip(bone_normalized, -2.0, 2.0)

    # Apply body scale adjustments from photo personalization
    scales = body_scale_adjustments or {}
    
    # Calculate overall scale from weight/height if available
    overall_scale = 1.0
    if body.height_cm and body.weight_kg:
        # BMI-based scaling
        bmi = body.weight_kg / ((body.height_cm / 100) ** 2)
        overall_scale = 0.8 + (bmi - 20) / 30.0  # Scale between 0.8 and 1.2
        overall_scale = np.clip(overall_scale, 0.7, 1.3)
        scales["overall"] = overall_scale

    return AvatarParameters(
        betas=betas.tolist(),
        scales=scales,
        notes="SMPL-X parameters generated from DEXA metrics with improved mapping",
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
    Produce a GLB file using SMPL-X if available, otherwise placeholder.
    Returns tuple of (avatar_id, glb_path, metadata_path) as relative paths.
    """

    avatar_id = uuid4().hex
    glb_path = OUTPUT_DIR / f"{avatar_id}.glb"

    # Convert betas to numpy array
    betas = np.array(parameters.betas, dtype=np.float32) if parameters.betas else np.zeros(10, dtype=np.float32)
    
    # Get overall scale from scales dict
    overall_scale = parameters.scales.get("overall", 1.0) if parameters.scales else 1.0
    
    # Try to generate SMPL-X mesh first
    mesh = generate_smplx_mesh(betas, scale=overall_scale, use_smplx=True)
    
    # Fallback to placeholder if SMPL-X not available
    if mesh is None:
        scale = overall_scale * (1.0 + float(betas[0]) * 0.1 if len(betas) > 0 else 1.0)
        mesh = _create_placeholder_mesh(scale)
    
    # Apply regional scale adjustments if provided
    if parameters.scales:
        for region, scale_factor in parameters.scales.items():
            if region != "overall":
                # Apply regional scaling (simplified - would need vertex selection in full implementation)
                pass  # TODO: Implement regional vertex scaling
    
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


