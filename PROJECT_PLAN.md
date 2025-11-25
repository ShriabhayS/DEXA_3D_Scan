# DEXA → 3D Avatar Conversion - Project Plan

## Overview
Convert DEXA scan data into accurate 3D human avatars with optional personalization and future state projection.

## Technical Architecture

### Phase 1: DEXA Scan Parsing & Data Extraction
**Goal**: Extract body composition metrics from PDF DEXA scans

**Approach**:
- Use PDF parsing libraries (PyPDF2, pdfplumber) to extract text/tables
- OCR (Tesseract/PaddleOCR) for scanned images if needed
- Extract key metrics:
  - Total body fat %
  - Lean mass (kg)
  - Bone mineral density (BMD)
  - Regional measurements (arms, legs, trunk)
  - Height/Weight if available
  - Android/Gynoid fat distribution

**Output**: Structured JSON with all extracted metrics

### Phase 2: 3D Avatar Generation
**Goal**: Convert metrics to anatomically accurate 3D mesh

**Approach**:
- Use parametric body model (SMPL-X or similar) as base
- Map DEXA metrics to body shape parameters:
  - Body fat % → body volume/thickness
  - Regional fat → localized shape adjustments
  - Lean mass → muscle definition
  - Bone density → skeletal structure visibility
- Generate watertight mesh
- Export as .glb format

**Key Metrics Mapping**:
- Body Fat % → Overall body volume (beta parameters in SMPL)
- Regional fat distribution → Vertex-level adjustments
- Lean mass → Muscle definition (shape parameters)
- Height/Weight → Scale and proportions

### Phase 3: Personalization (Optional)
**Goal**: Add face/body likeness from 2D photos

**Approach**:
- Face detection and landmark extraction (MediaPipe/Dlib)
- Face texture mapping onto avatar
- Body shape refinement from full-body photos
- Blend face texture with neutral avatar

### Phase 4: Future State Projection
**Goal**: Morph avatar between current and target states

**Approach**:
- Interpolate body shape parameters between states
- Target state calculation:
  - Target body fat % → new body volume
  - Target lean mass → new muscle definition
- Smooth vertex-level morphing
- Preserve anatomical correctness

### Phase 5: Viewer & Interface
**Goal**: Web-based 3D viewer with controls

**Approach**:
- Three.js for 3D rendering
- React/Next.js for UI
- Orbit controls (rotate/zoom/pan)
- Slider for morphing between states
- Screenshot functionality
- Mobile-responsive design

### Phase 6: Admin & Import System
**Goal**: Batch process DEXA scans

**Approach**:
- File upload interface
- Batch processing queue
- Progress tracking
- Export generated avatars

## Technology Stack

### Backend
- **Python 3.10+**
  - FastAPI (API server)
  - PyPDF2/pdfplumber (PDF parsing)
  - OpenCV/PIL (image processing)
  - MediaPipe (face detection)
  - SMPL-X or similar (3D body model)
  - trimesh/pymeshlab (mesh processing)
  - pygltflib (GLB export)

### Frontend
- **React/Next.js**
  - Three.js (3D rendering)
  - React Three Fiber (React wrapper)
  - Tailwind CSS (styling)
  - Zustand/Redux (state management)

### Infrastructure
- Docker (containerization)
- Local file storage (MVP)
- Optional: Cloud storage for production

## Project Structure

```
DEXA_3D_Scan/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI server
│   │   ├── dexa_parser.py       # PDF parsing & extraction
│   │   ├── avatar_generator.py  # 3D mesh generation
│   │   ├── personalization.py   # Face/body mapping
│   │   ├── morphing.py          # Future state projection
│   │   └── models.py            # Data models
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AvatarViewer.jsx
│   │   │   ├── Controls.jsx
│   │   │   └── UploadForm.jsx
│   │   ├── App.jsx
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
├── data/
│   └── samples/                 # DEXA scans & images
├── output/                      # Generated avatars
├── models/                      # 3D body models (SMPL-X)
├── README.md
└── docker-compose.yml
```

## Implementation Steps

### Week 1-2: Foundation
1. ✅ Set up project structure
2. ✅ DEXA PDF parser (extract metrics)
3. ✅ Basic 3D body model integration
4. ✅ Metric-to-shape parameter mapping

### Week 3-4: Core Features
5. ✅ Generate 3D avatar from metrics
6. ✅ GLB export functionality
7. ✅ Basic web viewer
8. ✅ Morphing system (current → target)

### Week 5: Personalization
9. ✅ Face detection & mapping
10. ✅ Body photo integration
11. ✅ Texture blending

### Week 6: Polish & Integration
12. ✅ Admin import interface
13. ✅ Batch processing
14. ✅ Mobile optimization
15. ✅ Testing & documentation

## Key Challenges & Solutions

1. **DEXA PDF Format Variability**
   - Solution: Robust parsing with multiple fallback methods
   - Manual correction interface if needed

2. **Metric-to-Shape Mapping Accuracy**
   - Solution: Calibrate using known body measurements
   - Iterative refinement with test cases

3. **Real-time Performance**
   - Solution: Pre-compute meshes, optimize GLB files
   - Use LOD (Level of Detail) for complex models

4. **Anatomical Correctness**
   - Solution: Constrain morphing within valid parameter ranges
   - Validate against medical reference data

## Success Metrics

- ✅ Accurate body composition representation (visual match to scan)
- ✅ Smooth morphing (60fps on modern devices)
- ✅ Recognizable personalization (user can identify themselves)
- ✅ Fast processing (< 30s per scan)
- ✅ Mobile-friendly viewer

## Next Steps

1. Initialize project structure
2. Set up development environment
3. Start with DEXA parser
4. Integrate 3D body model
5. Build MVP pipeline

