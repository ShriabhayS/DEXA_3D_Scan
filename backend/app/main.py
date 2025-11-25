"""
FastAPI backend for DEXA → 3D Avatar conversion pipeline.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .dexa_parser import parse_pdf_bytes, DexaParserError
from .avatar_generator import process_dexa_to_avatar
from .personalization import refine_parameters_with_photo
from .morphing import handle_morph_request
from .models import (
    AvatarGenerationRequest,
    AvatarGenerationResponse,
    BatchProcessRequest,
    BatchProcessResponse,
    MorphRequest,
    MorphResponse,
    DexaScanData,
)

app = FastAPI(
    title="DEXA to 3D Avatar API",
    description="Convert DEXA scan PDFs into personalized 3D avatars",
    version="1.0.0",
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount output directory for serving generated files
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "DEXA to 3D Avatar API"}


@app.post("/api/parse-dexa", response_model=DexaScanData)
async def parse_dexa_pdf(file: UploadFile = File(...)):
    """
    Parse a DEXA scan PDF and extract structured metrics.
    
    Note: This endpoint operates entirely in-memory:
    - UploadFile.read() loads file content into memory
    - parse_pdf_bytes() uses BytesIO (in-memory buffer)
    - No file system operations occur, so FileNotFoundError cannot be raised
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        pdf_bytes = await file.read()
        dexa_data = parse_pdf_bytes(pdf_bytes)
        return dexa_data
    except DexaParserError as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse DEXA PDF: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/generate-avatar", response_model=AvatarGenerationResponse)
async def generate_avatar(
    dexa_file: UploadFile = File(...),
    body_photo: Optional[UploadFile] = File(None),
    target_body_fat_percent: Optional[float] = None,
):
    """
    Generate a 3D avatar from a DEXA scan PDF, optionally with body photo personalization.
    """
    try:
        # Parse DEXA PDF
        pdf_bytes = await dexa_file.read()
        dexa_data = parse_pdf_bytes(pdf_bytes)

        # Handle body photo if provided
        body_scale_adjustments = None
        if body_photo:
            photo_path = OUTPUT_DIR / f"temp_photo_{uuid4().hex}.jpg"
            photo_bytes = await body_photo.read()
            # OUTPUT_DIR is created at module level, so FileNotFoundError should not occur
            # unless there's a permission issue (which would raise PermissionError instead)
            photo_path.write_bytes(photo_bytes)
            body_scale_adjustments = refine_parameters_with_photo(dexa_data, photo_path)
            # Clean up temp file
            photo_path.unlink(missing_ok=True)

        # Generate avatar
        response = process_dexa_to_avatar(dexa_data, body_scale_adjustments)

        # If target body fat is specified, we could generate a target state here
        # For now, we just return the current state
        if target_body_fat_percent:
            # This would trigger morphing logic in a future enhancement
            pass

        return response

    except DexaParserError as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse DEXA PDF: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/generate-avatar-from-data", response_model=AvatarGenerationResponse)
async def generate_avatar_from_data(request: AvatarGenerationRequest):
    """
    Generate a 3D avatar from pre-parsed DEXA data (useful for batch processing).
    """
    try:
        body_scale_adjustments = None
        if request.body_photo_metadata and request.body_photo_metadata.image_url:
            # In a real implementation, download the image from the URL
            # For MVP, we'll skip this if it's a URL
            pass

        response = process_dexa_to_avatar(request.dexa_data, body_scale_adjustments)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/morph", response_model=MorphResponse)
async def morph_avatar(request: MorphRequest):
    """
    Generate a morphing sequence between two avatar states.
    """
    try:
        response = handle_morph_request(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/avatar/{avatar_id}/glb")
async def get_avatar_glb(avatar_id: str):
    """
    Retrieve the GLB file for a generated avatar.
    """
    glb_path = OUTPUT_DIR / f"{avatar_id}.glb"
    if not glb_path.exists():
        raise HTTPException(status_code=404, detail="Avatar not found")
    return FileResponse(glb_path, media_type="model/gltf-binary")


@app.post("/api/batch-process", response_model=BatchProcessResponse)
async def batch_process(
    request: BatchProcessRequest,
    background_tasks: BackgroundTasks,
):
    """
    Process multiple DEXA PDFs in batch. Returns immediately with a job ID.
    """
    job_id = uuid4().hex
    processed: List[str] = []
    failed: Dict[str, str] = {}

    async def process_batch():
        for pdf_path in request.pdf_paths:
            path = Path(pdf_path)
            if not path.exists():
                failed[pdf_path] = "File not found"
                continue

            try:
                pdf_bytes = path.read_bytes()
                dexa_data = parse_pdf_bytes(pdf_bytes)
                response = process_dexa_to_avatar(dexa_data)
                processed.append(response.avatar_id)
            except Exception as e:
                failed[pdf_path] = str(e)

    background_tasks.add_task(process_batch)

    return BatchProcessResponse(
        job_id=job_id,
        processed=processed,
        failed=failed,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
