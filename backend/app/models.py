"""
Data models used across the DEXA → 3D avatar pipeline.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class DexaRegionMetrics(BaseModel):
    """Metrics for a specific anatomical region reported in a DEXA scan."""

    fat_mass_kg: Optional[float] = Field(None, ge=0)
    lean_mass_kg: Optional[float] = Field(None, ge=0)
    bone_mass_kg: Optional[float] = Field(None, ge=0)
    fat_percent: Optional[float] = Field(None, ge=0, le=100)


class DexaBodyMetrics(BaseModel):
    """Whole-body measurements extracted from DEXA or patient metadata."""

    height_cm: Optional[float] = Field(None, ge=50, le=250)
    weight_kg: Optional[float] = Field(None, ge=20, le=250)
    total_fat_percent: Optional[float] = Field(None, ge=0, le=80)
    total_lean_mass_kg: Optional[float] = Field(None, ge=0, le=200)
    total_bone_mass_kg: Optional[float] = Field(None, ge=0, le=50)
    android_fat_percent: Optional[float] = Field(None, ge=0, le=100)
    gynoid_fat_percent: Optional[float] = Field(None, ge=0, le=100)


class DexaScanData(BaseModel):
    """Canonical representation of a parsed DEXA report."""

    patient_id: Optional[str]
    scan_date: Optional[str]
    device_model: Optional[str]
    body_metrics: DexaBodyMetrics
    regions: Dict[str, DexaRegionMetrics] = Field(default_factory=dict)


class BodyPhotoMetadata(BaseModel):
    """Metadata for an optional body photo used for personalization."""

    image_url: Optional[HttpUrl]
    pose_reference: Optional[str]


class AvatarParameters(BaseModel):
    """Intermediate SMPL-X parameterization derived from DEXA data."""

    betas: List[float] = Field(default_factory=list, description="Shape coeffs")
    scales: Dict[str, float] = Field(
        default_factory=dict, description="Regional scale overrides"
    )
    notes: Optional[str]


class AvatarGenerationRequest(BaseModel):
    """Payload accepted by the FastAPI backend to trigger avatar generation."""

    dexa_data: DexaScanData
    target_body_fat_percent: Optional[float]
    body_photo_metadata: Optional[BodyPhotoMetadata]


class AvatarGenerationResponse(BaseModel):
    """Response returned after processing a DEXA scan."""

    avatar_id: str
    glb_path: str
    preview_image_path: Optional[str]
    parameters: AvatarParameters


class MorphRequest(BaseModel):
    """Request payload for morphing between two avatar states."""

    start_parameters: AvatarParameters
    end_parameters: AvatarParameters
    steps: int = Field(default=10, ge=2, le=120)


class MorphResponse(BaseModel):
    """Result of the morphing pipeline."""

    morph_sequence_paths: List[str]


class BatchProcessRequest(BaseModel):
    """Payload describing multiple DEXA scans scheduled for batch processing."""

    pdf_paths: List[str]


class BatchProcessResponse(BaseModel):
    """Batch-processing summary."""

    job_id: str
    processed: List[str]
    failed: Dict[str, str]


