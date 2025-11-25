# SMPL-X Model Setup Guide

## Overview

SMPL-X model files are **not included** in this repository due to licensing requirements. You need to download them separately from the official SMPL-X website.

## Getting SMPL-X Model Files

### Step 1: Register and Download

1. Visit the official SMPL-X website: https://smpl-x.is.tue.mpg.de/
2. Register for an account (free for non-commercial research)
3. Accept the license terms
4. Download the model files:
   - `SMPLX_NEUTRAL.pkl` (recommended for MVP)
   - `SMPLX_MALE.pkl` (optional)
   - `SMPLX_FEMALE.pkl` (optional)

### Step 2: Place Model Files

Place the downloaded `.pkl` files in the `models/` directory:

```
DEXA_3D_Scan/
└── models/
    ├── SMPLX_NEUTRAL.pkl
    ├── SMPLX_MALE.pkl (optional)
    └── SMPLX_FEMALE.pkl (optional)
```

### Step 3: Install Optional Dependencies

For full SMPL-X support, install the `smplx` library:

```bash
cd backend
pip install smplx chumpy
```

**Note**: The `smplx` library requires PyTorch. If you don't have PyTorch installed:

```bash
pip install torch torchvision
```

### Step 4: Verify Setup

The system will automatically detect and use SMPL-X models if:
- Model files are in `models/` directory
- Files are named correctly (SMPLX_NEUTRAL.pkl, etc.)

## How It Works

Our implementation supports two methods:

### Method 1: Using smplx Library (Preferred)
- Requires: `smplx` package installed
- More accurate mesh generation
- Full SMPL-X feature support
- Uses PyTorch for computation

### Method 2: Direct Pickle Loading (Fallback)
- Works without smplx library
- Basic mesh generation
- Simplified shape blending
- No PyTorch required

## Configuration

Set environment variable to use custom model directory:

```bash
export SMPLX_MODEL_DIR=/path/to/models
```

Or in Python:
```python
import os
os.environ["SMPLX_MODEL_DIR"] = "/path/to/models"
```

## Troubleshooting

### Model Not Found
- Check that model files are in `models/` directory
- Verify file names match: `SMPLX_NEUTRAL.pkl`
- Check file permissions

### Import Errors
- If `smplx` library not available, system falls back to pickle loading
- This is fine for MVP - placeholder meshes will be used if models unavailable

### PyTorch Issues
- If PyTorch not installed, only pickle loading will work
- For full features, install PyTorch: `pip install torch`

## License

**Important**: SMPL-X models are licensed for non-commercial research use only.

- Academic/Research: Free with registration
- Commercial: Requires separate license from ps-licensing@tue.mpg.de

See: https://smpl-x.is.tue.mpg.de/ for full license terms.

## References

- SMPL-X Official Site: https://smpl-x.is.tue.mpg.de/
- SMPLify-X Repository: https://github.com/vchoutas/smplify-x
- SMPL-X Paper: "Expressive Body Capture: 3D Hands, Face, and Body from a Single Image"

## Current Status

✅ Model loading infrastructure implemented
✅ Automatic fallback to placeholder if models unavailable
✅ Support for both smplx library and direct pickle loading
⏳ Model files need to be downloaded separately
⏳ smplx library installation optional but recommended

