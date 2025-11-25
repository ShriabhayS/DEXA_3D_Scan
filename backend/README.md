# Backend Overview

This FastAPI backend ingests DEXA scan PDFs and optional body photos, converts
the structured metrics into SMPL-X body parameters, generates a watertight GLB
avatar, and exposes endpoints for morphing, batch processing, and asset
retrieval.

## Key Modules

| File | Description |
| --- | --- |
| `app/main.py` | FastAPI application with processing endpoints |
| `app/models.py` | Pydantic schemas for DEXA data, requests, and responses |
| `app/dexa_parser.py` | PDF parsing utilities using `pdfplumber` |
| `app/avatar_generator.py` | Mapping logic from DEXA metrics to SMPL-X params |
| `app/personalization.py` | Body/face personalization via photo landmarks |
| `app/morphing.py` | Future-state interpolation utilities |

## Development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `SMPLX_MODEL_DIR` | Filesystem path to the downloaded SMPL-X model bundle |
| `OUTPUT_DIR` | Directory for generated GLB/preview assets (`output/` default) |

## Notes

- SMPL-X assets are not bundled; obtain them from https://smpl-x.is.tue.mpg.de/
- The current implementation uses placeholder mapping logic so the pipeline can
  be exercised without licensed assets. Replace TODO sections with real model
  code once the assets are available.

