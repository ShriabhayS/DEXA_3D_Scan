# DEXA to 3D Avatar MVP

Convert DEXA scan PDFs into personalized 3D human avatars with body shape personalization, future state projection, and an interactive web viewer.

## Features

- **DEXA PDF Parsing**: Extract body composition metrics from DEXA scan PDFs
- **3D Avatar Generation**: Convert DEXA metrics into anatomically accurate 3D meshes
- **Body Personalization**: Refine avatar proportions using full-body photos
- **Future State Projection**: Morph between current and target body states
- **Interactive Viewer**: Web-based 3D viewer with orbit controls and morphing slider
- **Batch Processing**: Process multiple DEXA scans asynchronously

## Project Structure

```
DEXA_3D_Scan/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py              # FastAPI server
│   │   ├── dexa_parser.py       # PDF parsing & extraction
│   │   ├── avatar_generator.py  # DEXA → 3D conversion
│   │   ├── personalization.py   # Body/face photo integration
│   │   ├── morphing.py          # Future state projection
│   │   └── models.py            # Data models (Pydantic)
│   ├── requirements.txt
│   └── README.md
├── frontend/             # React + Three.js frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── AvatarViewer.jsx
│   │   │   ├── Controls.jsx
│   │   │   └── UploadForm.jsx
│   │   ├── App.jsx
│   │   └── utils/
│   ├── package.json
│   └── README.md
├── data/
│   └── samples/         # Sample DEXA scans
├── models/              # SMPL-X model files (not included)
├── output/              # Generated avatars
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up SMPL-X models (optional):
   - Download SMPL-X models from https://smpl-x.is.tue.mpg.de/
   - Place model files in the `models/` directory
   - Set `SMPLX_MODEL_DIR` environment variable if using a custom path

5. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Upload DEXA Scan**: Use the upload form to select a DEXA scan PDF
2. **Optional Personalization**: Upload a full-body photo to refine avatar proportions
3. **Set Target State**: Optionally specify a target body fat percentage for morphing
4. **View Avatar**: Interact with the 3D avatar using mouse controls
5. **Morph**: Use the slider to morph between current and target states
6. **Export**: Download the GLB file or take a screenshot

## API Endpoints

- `POST /api/parse-dexa` - Parse a DEXA PDF and extract metrics
- `POST /api/generate-avatar` - Generate a 3D avatar from DEXA scan
- `POST /api/generate-avatar-from-data` - Generate avatar from pre-parsed data
- `POST /api/morph` - Generate morphing sequence between states
- `GET /api/avatar/{avatar_id}/glb` - Retrieve GLB file
- `POST /api/batch-process` - Process multiple DEXA scans

See `backend/README.md` for detailed API documentation.

## Technical Details

### DEXA Parsing

The parser uses `pdfplumber` to extract text from DEXA PDFs and regex patterns to identify key metrics:
- Total body fat percentage
- Lean mass and bone mass
- Regional measurements (arms, legs, trunk, android, gynoid)
- Height and weight (if available)

### 3D Avatar Generation

Currently uses a placeholder mesh generation approach. For production, integrate SMPL-X models:
- Map DEXA metrics to SMPL-X beta parameters
- Generate anatomically correct 3D meshes
- Export as GLB format for web viewing

### Body Personalization

Uses MediaPipe Pose to extract body measurements from photos:
- Shoulder width, hip width, torso length
- Maps measurements to SMPL-X scale parameters
- Blends photo-derived shape with DEXA-derived shape

### Future State Projection

Interpolates between current and target body parameters:
- Linear interpolation of beta parameters
- Smooth morphing between meshes
- Preserves anatomical correctness

## Development

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Testing

Test the DEXA parser with sample PDFs:
```bash
python -m pytest backend/tests/  # If tests exist
```

## Environment Variables

- `SMPLX_MODEL_DIR` - Path to SMPL-X model files (default: `models/`)
- `OUTPUT_DIR` - Directory for generated avatars (default: `output/`)

## Limitations & Future Work

- **SMPL-X Integration**: Currently uses placeholder meshes. Full SMPL-X integration needed for production.
- **Face Personalization**: Stretch goal - not yet implemented
- **Advanced Morphing**: Current morphing is simplified. Full mesh interpolation needed.
- **Error Handling**: Basic error handling implemented. More robust validation needed.
- **Performance**: Processing is synchronous. Async processing queue needed for scale.

## License

This project is for MVP/demonstration purposes. SMPL-X models require separate licensing from MPI-IS.

## Contributing

This is an MVP implementation. For production use, consider:
- Full SMPL-X model integration
- Enhanced error handling and validation
- Performance optimization
- Security hardening
- Cloud storage integration

