"""
Future-state projection and morphing utilities.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np

from .models import AvatarParameters, MorphRequest, MorphResponse


def interpolate_parameters(
    start: AvatarParameters, end: AvatarParameters, steps: int
) -> List[AvatarParameters]:
    start_betas = np.array(start.betas, dtype=np.float32)
    end_betas = np.array(end.betas, dtype=np.float32)

    if start_betas.shape != end_betas.shape:
        raise ValueError("Parameter vectors must have identical shapes")

    interpolated: List[AvatarParameters] = []
    for t in np.linspace(0.0, 1.0, steps):
        betas = start_betas * (1 - t) + end_betas * t
        scales = {
            key: start.scales.get(key, 1.0) * (1 - t)
            + end.scales.get(key, 1.0) * t
            for key in set(start.scales) | set(end.scales)
        }
        interpolated.append(AvatarParameters(betas=betas.tolist(), scales=scales))
    return interpolated


def handle_morph_request(request: MorphRequest) -> MorphResponse:
    sequence = interpolate_parameters(request.start_parameters, request.end_parameters, request.steps)
    # For the MVP we simply persist the parameter snapshots for downstream rendering.
    morph_dir = Path("output/morphs")
    morph_dir.mkdir(parents=True, exist_ok=True)
    paths: List[str] = []
    for idx, params in enumerate(sequence):
        path = morph_dir / f"morph_{idx:03d}.json"
        path.write_text(params.json(indent=2))
        paths.append(str(path))
    return MorphResponse(morph_sequence_paths=paths)


