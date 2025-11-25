"""
Future-state projection and morphing utilities.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import numpy as np
import trimesh

from .models import AvatarParameters, MorphRequest, MorphResponse
from .avatar_generator import generate_avatar_assets


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


def interpolate_meshes(
    start_mesh: trimesh.Trimesh,
    end_mesh: trimesh.Trimesh,
    steps: int,
) -> List[trimesh.Trimesh]:
    """
    Interpolate between two meshes at the vertex level.
    
    Args:
        start_mesh: Starting mesh
        end_mesh: Target mesh
        steps: Number of interpolation steps
        
    Returns:
        List of interpolated meshes
    """
    if start_mesh.vertices.shape != end_mesh.vertices.shape:
        raise ValueError("Meshes must have the same vertex count for interpolation")
    
    if start_mesh.faces.shape != end_mesh.faces.shape:
        raise ValueError("Meshes must have the same face structure")
    
    interpolated_meshes = []
    start_verts = start_mesh.vertices
    end_verts = end_mesh.vertices
    
    for t in np.linspace(0.0, 1.0, steps):
        # Linear interpolation of vertices
        interp_verts = start_verts * (1 - t) + end_verts * t
        
        # Create new mesh with interpolated vertices
        interp_mesh = trimesh.Trimesh(
            vertices=interp_verts,
            faces=start_mesh.faces.copy(),
            vertex_normals=start_mesh.vertex_normals.copy() if hasattr(start_mesh, 'vertex_normals') else None
        )
        interpolated_meshes.append(interp_mesh)
    
    return interpolated_meshes


def handle_morph_request(request: MorphRequest, generate_meshes: bool = True) -> MorphResponse:
    """
    Handle a morphing request between two avatar states.
    
    Args:
        request: Morph request with start/end parameters
        generate_meshes: If True, generate GLB files for each step
        
    Returns:
        Morph response with paths to generated files
    """
    sequence = interpolate_parameters(request.start_parameters, request.end_parameters, request.steps)
    morph_dir = Path("output/morphs")
    morph_dir.mkdir(parents=True, exist_ok=True)
    paths: List[str] = []
    
    if generate_meshes:
        # Generate meshes for start and end states
        _, start_glb, _ = generate_avatar_assets(request.start_parameters)
        _, end_glb, _ = generate_avatar_assets(request.end_parameters)
        
        # Load meshes
        start_mesh = trimesh.load(Path(start_glb))
        end_mesh = trimesh.load(Path(end_glb))
        
        # Interpolate meshes
        morph_meshes = interpolate_meshes(start_mesh, end_mesh, request.steps)
        
        # Save interpolated meshes
        for idx, mesh in enumerate(morph_meshes):
            glb_path = morph_dir / f"morph_{idx:03d}.glb"
            scene = trimesh.Scene(mesh)
            scene.export(glb_path, file_type="glb")
            paths.append(str(glb_path))
    else:
        # Just save parameter files (legacy behavior)
        for idx, params in enumerate(sequence):
            path = morph_dir / f"morph_{idx:03d}.json"
            path.write_text(params.json(indent=2))
            paths.append(str(path))
    
    return MorphResponse(morph_sequence_paths=paths)


