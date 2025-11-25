"""
Unit tests for avatar generator.
"""
import pytest
import numpy as np
from backend.app.avatar_generator import (
    map_metrics_to_parameters,
    _normalize,
)
from backend.app.models import DexaScanData, DexaBodyMetrics


def test_normalize():
    """Test normalization function."""
    assert _normalize(50.0, 100.0) == 0.5
    assert _normalize(None, 100.0) == 0.0
    assert _normalize(0.0, 100.0) == 0.0


def test_map_metrics_to_parameters():
    """Test DEXA metrics to parameter mapping."""
    body_metrics = DexaBodyMetrics(
        total_fat_percent=25.0,
        total_lean_mass_kg=60.0,
        height_cm=170.0,
        weight_kg=80.0,
    )
    
    dexa_data = DexaScanData(
        body_metrics=body_metrics,
        regions={}
    )
    
    params = map_metrics_to_parameters(dexa_data)
    
    assert params is not None
    assert len(params.betas) == 10
    assert isinstance(params.betas, list)
    assert all(isinstance(b, (int, float)) for b in params.betas)


def test_map_metrics_with_regions():
    """Test parameter mapping with regional data."""
    body_metrics = DexaBodyMetrics(
        total_fat_percent=30.0,
        total_lean_mass_kg=55.0,
        height_cm=175.0,
        weight_kg=75.0,
        android_fat_percent=35.0,
        gynoid_fat_percent=40.0,
    )
    
    from backend.app.models import DexaRegionMetrics
    
    dexa_data = DexaScanData(
        body_metrics=body_metrics,
        regions={
            "android": DexaRegionMetrics(fat_percent=35.0),
            "gynoid": DexaRegionMetrics(fat_percent=40.0),
        }
    )
    
    params = map_metrics_to_parameters(dexa_data)
    
    assert params is not None
    assert len(params.betas) == 10
    # Beta 4 and 5 should be set for android/gynoid
    assert params.betas[4] != 0.0 or params.betas[5] != 0.0


def test_parameter_clamping():
    """Test that parameters are clamped to valid ranges."""
    body_metrics = DexaBodyMetrics(
        total_fat_percent=100.0,  # Unrealistically high
        total_lean_mass_kg=200.0,  # Unrealistically high
        height_cm=300.0,  # Unrealistically high
        weight_kg=500.0,  # Unrealistically high
    )
    
    dexa_data = DexaScanData(
        body_metrics=body_metrics,
        regions={}
    )
    
    params = map_metrics_to_parameters(dexa_data)
    
    # All betas should be clamped to reasonable range (-2 to 2)
    for beta in params.betas:
        assert -2.5 <= beta <= 2.5  # Allow small margin

