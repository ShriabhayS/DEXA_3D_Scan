# DEXA to 3D Avatar

Convert DEXA scan PDFs into personalized 3D human avatars with body shape personalization, future state projection, and an interactive web viewer.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start) - Get started locally
- [Installation](#installation) - Set up on your machine
- [Usage](#usage) - How to use (local vs production)
- [Deployment](#deployment) - Deploy to production (Vercel + backend)
- [SMPL-X Model Setup](#smpl-x-model-setup) - Optional: Add realistic avatars
- [Testing](#testing) - Verify everything works
- [API Documentation](#api-documentation) - Backend API reference
- [Troubleshooting](#troubleshooting) - Common issues and solutions
- [Technical Details](#technical-details) - How it works
- [Project Status](#project-status) - What's done and what's next

## Features

- **DEXA PDF Parsing**: Extract body composition metrics from DEXA scan PDFs
- **3D Avatar Generation**: Convert DEXA metrics into 3D meshes (SMPL-X when available, placeholder otherwise)
- **Body Personalization**: Refine avatar proportions using full-body photos
- **Future State Projection**: Morph between current and target body states
- **Interactive Viewer**: Web-based 3D viewer with orbit controls and morphing slider
- **Screenshot**: Capture and download avatar images
- **Batch Processing**: Process multiple DEXA scans asynchronously

## Project Structure

```
DEXA_3D_Scan/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py              # FastAPI server
│   │   ├── dexa_parser.py       # PDF parsing & extraction
│   │   ├── avatar_generator.py  # DEXA → 3D conversion
│   │   ├── smplx_loader.py      # SMPL-X model loading
│   │   ├── personalization.py   # Body photo integration
│   │   ├── morphing.py          # Future state projection
│   │   └── models.py            # Data models (Pydantic)
│   ├── tests/                   # Unit tests
│   ├── requirements.txt
│   └── README.md
├── frontend/             # React + Three.js frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── AvatarViewer.jsx  # 3D viewer
│   │   │   ├── Controls.jsx     # Morphing controls
│   │   │   └── UploadForm.jsx   # File upload
│   │   ├── App.jsx
│   │   └── utils/
│   ├── package.json
│   ├── vercel.json              # Vercel deployment config
│   └── README.md
├── data/
│   └── samples/         # Sample DEXA scans
├── models/              # SMPL-X model files (not included, see setup)
├── output/              # Generated avatars
└── README.md
```

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **npm** or **yarn**

### Installation

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

#### 3. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
.venv\Scripts\activate  # Windows (or source .venv/bin/activate on macOS/Linux)
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

#### 4. Access the Application

**Local Development (on your machine)**:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

**Note**: These URLs only work on your local machine. For production deployment, see the [Deployment](#deployment) section below.

## Usage

### Local Development

When running locally, access the application at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

### Production Deployment

Once deployed (see [Deployment](#deployment) section), access the application via:
- **Frontend**: `https://your-project.vercel.app` (your Vercel URL)
- **Backend API**: `https://your-backend.railway.app` (your backend URL)

### Basic Workflow

1. **Open the application**:
   - **Local**: http://localhost:3000
   - **Production**: Your Vercel URL (e.g., `https://your-project.vercel.app`)
2. **Upload a DEXA scan PDF** using the file picker
3. **(Optional) Upload a body photo** for personalization
4. **(Optional) Enter target body fat %** for morphing
5. **Click "Generate Avatar"** and wait for processing (5-10 seconds)
6. **Interact with the 3D avatar**:
   - **Left-click + drag**: Rotate
   - **Scroll**: Zoom in/out
   - **Right-click + drag**: Pan
7. **Use the morph slider** to see transitions between current and target states
8. **Download the GLB file** or take a screenshot

### Sample Data

Test with sample DEXA PDFs in `data/samples/`:
- `194_REES_Beau_.pdf`
- `196_ISMAIL_Nahla_.pdf`
- `205_GILDER_Bradley_.pdf`

## Deployment

### Frontend Deployment (Vercel)

1. **Connect Repository**:
   - Go to https://vercel.com
   - Sign in with GitHub
   - Click "New Project"
   - Import `DEXA_3D_Scan` repository
   - Set **Root Directory** to `frontend`

2. **Configure Build**:
   - Vercel will auto-detect Vite
   - Verify build command: `npm run build`
   - Verify output directory: `dist`

3. **Set Environment Variables**:
   - Add `VITE_API_URL` = Your backend URL (e.g., `https://your-backend.railway.app`)
   - **Important**: Do NOT include trailing slash

4. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete
   - Your frontend will be live at `https://your-project.vercel.app`

### Backend Deployment

#### Option 1: Railway (Recommended)

1. **Sign up** at https://railway.app and connect GitHub
2. **Create New Project** → "Deploy from GitHub repo"
3. **Select repository** and set root directory to `backend`
4. **Configure**:
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment variables:
     - `OUTPUT_DIR` = `/app/output` (optional)
     - `SMPLX_MODEL_DIR` = `/app/models` (if using models)
     - `CORS_ORIGINS` = Your Vercel frontend URL
5. **Deploy** and get the generated URL
6. **Update** `VITE_API_URL` in Vercel with the backend URL

#### Option 2: Render

1. **Sign up** at https://render.com and connect GitHub
2. **Create Web Service**:
   - Connect `DEXA_3D_Scan` repository
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Add environment variables** (same as Railway)
4. **Deploy** and update frontend `VITE_API_URL`

### Post-Deployment Testing

- [ ] Test backend API: `https://your-backend.railway.app/docs`
- [ ] Test frontend: `https://your-project.vercel.app`
- [ ] Test DEXA PDF upload
- [ ] Test avatar generation
- [ ] Test 3D viewer
- [ ] Verify CORS is working

## SMPL-X Model Setup

For realistic human body avatars, you can integrate SMPL-X models (optional).

### Step 1: Download Models

1. Visit https://smpl-x.is.tue.mpg.de/
2. Register for an account (free for non-commercial research)
3. Accept the license terms
4. Download model files:
   - `SMPLX_NEUTRAL.pkl` (recommended)
   - `SMPLX_MALE.pkl` (optional)
   - `SMPLX_FEMALE.pkl` (optional)

### Step 2: Place Model Files

Place downloaded `.pkl` files in the `models/` directory:

```
DEXA_3D_Scan/
└── models/
    ├── SMPLX_NEUTRAL.pkl
    ├── SMPLX_MALE.pkl (optional)
    └── SMPLX_FEMALE.pkl (optional)
```

### Step 3: Install Optional Dependencies

For full SMPL-X support:

```bash
cd backend
pip install smplx chumpy torch torchvision
```

**Note**: The system works without these - it will use placeholder meshes if models are unavailable.

### How It Works

- **Method 1 (Preferred)**: Uses `smplx` library if installed - more accurate
- **Method 2 (Fallback)**: Direct pickle loading - works without library
- **Method 3 (Default)**: Placeholder meshes if models not found

The system automatically detects and uses available models.

### License

SMPL-X models are licensed for **non-commercial research use only**:
- Academic/Research: Free with registration
- Commercial: Requires license from ps-licensing@tue.mpg.de

## Testing

### Verify Setup

Run the verification script:

```bash
python verify_setup.py
```

### Test Backend

```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Test health endpoint
curl http://localhost:8000/

# Test DEXA parsing
curl -X POST "http://localhost:8000/api/parse-dexa" \
  -F "file=@../data/samples/194_REES_Beau_.pdf"
```

### Test Frontend

1. Start frontend: `npm run dev`
2. Open http://localhost:3000
3. Upload a sample DEXA PDF
4. Verify avatar generation and viewing

### Run Unit Tests

```bash
cd backend
pytest tests/
```

## API Documentation

### Endpoints

- **`POST /api/parse-dexa`** - Parse a DEXA PDF and extract metrics
  - Request: `multipart/form-data` with `file` (PDF)
  - Response: `DexaScanData` JSON

- **`POST /api/generate-avatar`** - Generate a 3D avatar from DEXA scan
  - Request: `multipart/form-data` with:
    - `dexa_file` (required): DEXA PDF
    - `body_photo` (optional): Body photo for personalization
    - `target_body_fat_percent` (optional): Target body fat %
  - Response: `AvatarGenerationResponse` with `avatar_id` and `glb_path`

- **`POST /api/morph`** - Generate morphing sequence between states
  - Request: `MorphRequest` JSON with start/end parameters
  - Response: `MorphResponse` with morph sequence paths

- **`GET /api/avatar/{avatar_id}/glb`** - Download GLB file
  - Response: GLB file download

- **`POST /api/batch-process`** - Process multiple DEXA scans
  - Request: `BatchProcessRequest` with PDF paths
  - Response: `BatchProcessResponse` with job status

### Interactive API Docs

Visit http://localhost:8000/docs for interactive Swagger documentation.

## Troubleshooting

### Backend Issues

**Import errors**:
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

**Port already in use**:
```bash
uvicorn app.main:app --reload --port 8001
```

**DEXA parsing fails**:
- Ensure PDF has selectable text (not just scanned images)
- Check PDF format matches expected DEXA report structure
- Review extracted text in parser logs

### Frontend Issues

**Module not found**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**CORS errors**:
- Verify backend is running
- Check CORS configuration in `backend/app/main.py`
- Ensure frontend URL is allowed in backend CORS settings

**Avatar not displaying**:
- Check browser console for errors
- Verify GLB file exists in `output/` directory
- Check network tab for failed requests

### Deployment Issues

**Build fails on Vercel**:
- Check Node.js version (need 18+)
- Verify all dependencies in `package.json`
- Check build logs in Vercel dashboard

**API calls fail in production**:
- Verify `VITE_API_URL` is set correctly in Vercel
- Check backend CORS allows your Vercel domain
- Test backend API directly: `https://your-backend.railway.app/docs`

**Backend deployment fails**:
- Verify Python version (need 3.10+)
- Check all dependencies in `requirements.txt`
- Review deployment logs for specific errors

## Technical Details

### DEXA Parsing

The parser uses `pdfplumber` to extract text from DEXA PDFs and regex patterns to identify:
- Total body fat percentage
- Lean mass and bone mass
- Regional measurements (arms, legs, trunk, android, gynoid)
- Height and weight (if available)

### 3D Avatar Generation

- **SMPL-X Integration**: When model files are available, uses SMPL-X for realistic human bodies
- **Parameter Mapping**: Maps DEXA metrics to SMPL-X beta parameters (10 shape parameters)
- **Placeholder Fallback**: Uses simple meshes when SMPL-X models unavailable
- **Export Format**: GLB files for web compatibility

### Body Personalization

Uses MediaPipe Pose to extract body measurements from photos:
- Shoulder width, hip width, torso length
- Maps measurements to SMPL-X scale parameters
- Blends photo-derived shape with DEXA-derived shape

### Morphing

- **Vertex-level interpolation**: Smooth transitions between mesh states
- **Parameter interpolation**: Linear interpolation of beta parameters
- **Real-time preview**: Slider controls morphing progress

### Environment Variables

**Backend**:
- `SMPLX_MODEL_DIR` - Path to SMPL-X model files (default: `models/`)
- `OUTPUT_DIR` - Directory for generated avatars (default: `output/`)
- `CORS_ORIGINS` - Allowed frontend origins (default: `*`)

**Frontend**:
- `VITE_API_URL` - Backend API URL (default: `http://localhost:8000`)

## Project Status

### ✅ Completed Features

- DEXA PDF parsing and metric extraction
- 3D avatar generation (SMPL-X when available, placeholder otherwise)
- Enhanced parameter mapping (DEXA → SMPL-X beta parameters)
- Full mesh morphing with vertex interpolation
- Body photo personalization
- Web-based 3D viewer with interactive controls
- Screenshot functionality
- Batch processing API
- Comprehensive error handling
- Basic testing suite
- Vercel deployment configuration

### ⏳ Optional Enhancements

- Performance optimization (async queue, caching)
- Face personalization (stretch goal)
- Advanced camera controls
- Material customization
- Mobile touch controls
- More comprehensive test coverage

### 📋 Next Steps

1. **Deploy Backend**: Choose platform (Railway recommended) and deploy
2. **Deploy Frontend**: Deploy to Vercel with backend URL
3. **Download SMPL-X Models**: For realistic avatars (optional)
4. **Test End-to-End**: Verify full pipeline works in production

## License

This project is for MVP/demonstration purposes. SMPL-X models require separate licensing from MPI-IS for commercial use.

## Contributing

This is an MVP implementation. For production use, consider:
- Full SMPL-X model integration
- Enhanced error handling and validation
- Performance optimization
- Security hardening
- Cloud storage integration

## Support

For issues or questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review API documentation at `/docs` endpoint
- Check deployment logs for errors

---

**Ready to get started?** Follow the [Quick Start](#quick-start) guide above!
