"""
SMPL-X model loading and mesh generation utilities.

This module provides infrastructure for loading SMPL-X models and generating
3D meshes from body shape parameters (betas).

Based on the smplify-x repository: https://github.com/vchoutas/smplify-x

Note: SMPL-X models must be obtained separately from https://smpl-x.is.tue.mpg.de/
Place model files in the models/ directory or set SMPLX_MODEL_DIR environment variable.

The model files should be named:
- SMPLX_NEUTRAL.pkl (or SMPLX_MALE.pkl, SMPLX_FEMALE.pkl)
"""
from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Optional

import numpy as np
import trimesh

# Try to import SMPL-X library (smplx package)
try:
    import smplx
    SMPLX_LIBRARY_AVAILABLE = True
except ImportError:
    SMPLX_LIBRARY_AVAILABLE = False
    smplx = None

# Try to import PyTorch (required by smplx library)
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

SMPLX_MODEL_DIR = Path(os.getenv("SMPLX_MODEL_DIR", "models"))
SMPLX_MODEL_PATH = SMPLX_MODEL_DIR / "SMPLX_NEUTRAL.pkl"


class SMPLXModel:
    """Wrapper for SMPL-X model loading and mesh generation."""

    def __init__(self, model_path: Optional[Path] = None, gender: str = "neutral"):
        """
        Initialize SMPL-X model loader.

        Args:
            model_path: Path to SMPL-X model directory. If None, uses default path.
            gender: Model gender ('neutral', 'male', or 'female')
        """
        self.model_path = model_path or SMPLX_MODEL_DIR
        self.gender = gender
        self.model_data = None
        self.smplx_model = None
        self.loaded = False
        self.use_library = SMPLX_LIBRARY_AVAILABLE and TORCH_AVAILABLE

    def _find_model_file(self) -> Optional[Path]:
        """Find the appropriate SMPL-X model file."""
        # Try different model file names
        model_names = [
            f"SMPLX_{self.gender.upper()}.pkl",
            "SMPLX_NEUTRAL.pkl",
            "SMPLX.pkl",
        ]
        
        for name in model_names:
            model_file = self.model_path / name
            if model_file.exists():
                return model_file
        
        # Also check if model_path is a file directly
        if self.model_path.is_file():
            return self.model_path
        
        return None

    def is_available(self) -> bool:
        """Check if SMPL-X model files are available."""
        model_file = self._find_model_file()
        return model_file is not None and model_file.exists()

    def load_model(self) -> bool:
        """
        Load SMPL-X model from file.

        Returns:
            True if model loaded successfully, False otherwise.
        """
        if not self.is_available():
            return False

        model_file = self._find_model_file()
        if not model_file:
            return False

        try:
            if self.use_library:
                # Use smplx library (preferred method)
                return self._load_with_library(model_file)
            else:
                # Fallback: load pickle file directly
                return self._load_from_pickle(model_file)
        except Exception as e:
            print(f"Failed to load SMPL-X model: {e}")
            return False

    def _load_with_library(self, model_file: Path) -> bool:
        """Load model using smplx library (preferred method)."""
        try:
            # smplx library expects model folder, not file
            model_folder = model_file.parent
            
            # Create smplx model instance
            self.smplx_model = smplx.create(
                model_path=str(model_folder),
                model_type='smplx',
                gender=self.gender,
                use_face_contour=False,
                num_betas=10,  # Use 10 shape parameters
                ext='pkl',
            )
            self.loaded = True
            return True
        except Exception as e:
            print(f"Failed to load with smplx library: {e}")
            # Fallback to pickle loading
            return self._load_from_pickle(model_file)

    def _load_from_pickle(self, model_file: Path) -> bool:
        """Load model from pickle file (fallback method)."""
        try:
            with open(model_file, "rb") as f:
                self.model_data = pickle.load(f, encoding="latin1")
            self.loaded = True
            return True
        except Exception as e:
            print(f"Failed to load from pickle: {e}")
            return False

    def generate_mesh(
        self,
        betas: np.ndarray,
        pose: Optional[np.ndarray] = None,
        global_orient: Optional[np.ndarray] = None,
        scale: float = 1.0,
    ) -> Optional[trimesh.Trimesh]:
        """
        Generate a 3D mesh from SMPL-X parameters.

        Args:
            betas: Shape parameters (10 dimensions recommended)
            pose: Pose parameters (21 joints * 3 = 63 dimensions, optional)
            global_orient: Global rotation (3 dimensions, optional)
            scale: Overall scale factor

        Returns:
            Trimesh object or None if generation fails.
        """
        if not self.loaded:
            if not self.load_model():
                return None

        try:
            if self.smplx_model is not None:
                # Use smplx library for mesh generation
                return self._generate_with_library(betas, pose, global_orient, scale)
            elif self.model_data is not None:
                # Use pickle-loaded data
                return self._generate_from_pickle(betas, scale)
            else:
                return None
        except Exception as e:
            print(f"Error generating SMPL-X mesh: {e}")
            return None

    def _generate_with_library(
        self,
        betas: np.ndarray,
        pose: Optional[np.ndarray],
        global_orient: Optional[np.ndarray],
        scale: float,
    ) -> Optional[trimesh.Trimesh]:
        """Generate mesh using smplx library."""
        try:
            # Convert numpy to torch tensors
            betas_tensor = torch.from_numpy(betas.astype(np.float32)).unsqueeze(0)
            
            # Default pose (T-pose) if not provided
            if pose is None:
                body_pose = torch.zeros((1, 63), dtype=torch.float32)
            else:
                body_pose = torch.from_numpy(pose.astype(np.float32)).unsqueeze(0)
            
            # Default global orientation if not provided
            if global_orient is None:
                global_orient_tensor = torch.zeros((1, 3), dtype=torch.float32)
            else:
                global_orient_tensor = torch.from_numpy(global_orient.astype(np.float32)).unsqueeze(0)
            
            # Generate mesh
            output = self.smplx_model(
                betas=betas_tensor,
                body_pose=body_pose,
                global_orient=global_orient_tensor,
            )
            
            # Extract vertices and faces
            vertices = output.vertices[0].detach().cpu().numpy()
            faces = self.smplx_model.faces
            
            # Create trimesh
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            mesh.apply_scale(scale)
            
            return mesh
        except Exception as e:
            print(f"Error generating mesh with library: {e}")
            return None

    def _generate_from_pickle(self, betas: np.ndarray, scale: float) -> Optional[trimesh.Trimesh]:
        """Generate mesh from pickle-loaded model data."""
        try:
            if "v_template" not in self.model_data:
                return None

            # Apply shape blend shapes
            vertices = self._apply_shape_blend(betas)
            faces = self.model_data.get("f", None)

            if faces is None:
                return None

            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            mesh.apply_scale(scale)
            return mesh
        except Exception as e:
            print(f"Error generating mesh from pickle: {e}")
            return None

    def _apply_shape_blend(self, betas: np.ndarray) -> np.ndarray:
        """
        Apply shape blend shapes to template vertices.

        This implements the SMPL-X shape blending formula:
        v_shaped = v_template + sum(betas[i] * shapedirs[i])
        """
        if not self.model_data or "v_template" not in self.model_data:
            raise ValueError("Model data not loaded or invalid")

        v_template = self.model_data["v_template"]
        shapedirs = self.model_data.get("shapedirs", None)

        if shapedirs is None:
            # No shape blend shapes, return template
            return v_template.copy()

        # Ensure betas is the right size
        if len(betas) > shapedirs.shape[-1]:
            betas = betas[:shapedirs.shape[-1]]
        elif len(betas) < shapedirs.shape[-1]:
            # Pad with zeros
            betas_padded = np.zeros(shapedirs.shape[-1])
            betas_padded[:len(betas)] = betas
            betas = betas_padded

        # Apply shape blend shapes
        # shapedirs shape: (num_vertices, 3, num_betas)
        # betas shape: (num_betas,)
        # Result: (num_vertices, 3)
        v_shaped = v_template + np.einsum('vij,j->vi', shapedirs, betas)

        return v_shaped


# Global model instance (lazy loading)
_smplx_model: Optional[SMPLXModel] = None


def get_smplx_model(gender: str = "neutral") -> Optional[SMPLXModel]:
    """Get or create global SMPL-X model instance."""
    global _smplx_model
    if _smplx_model is None:
        _smplx_model = SMPLXModel(gender=gender)
    return _smplx_model


def generate_smplx_mesh(
    betas: np.ndarray,
    scale: float = 1.0,
    use_smplx: bool = True,
    gender: str = "neutral",
) -> Optional[trimesh.Trimesh]:
    """
    Generate a mesh using SMPL-X if available, otherwise return None.

    Args:
        betas: Shape parameters (10 dimensions)
        scale: Overall scale
        use_smplx: Whether to attempt SMPL-X generation
        gender: Model gender ('neutral', 'male', or 'female')

    Returns:
        Trimesh if SMPL-X available and successful, None otherwise.
    """
    if not use_smplx:
        return None

    model = get_smplx_model(gender=gender)
    if model and model.is_available():
        return model.generate_mesh(betas, scale=scale)

    return None
