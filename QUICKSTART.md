# Quick Start Guide

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn

## Installation

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Start Backend Server

```bash
# From backend directory
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Start Frontend Development Server

```bash
# From frontend directory (in a new terminal)
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Open `http://localhost:3000` in your browser
2. Click "Choose File" and select a DEXA scan PDF
3. (Optional) Upload a body photo for personalization
4. (Optional) Enter a target body fat percentage
5. Click "Generate Avatar"
6. Wait for processing (usually 5-10 seconds)
7. Interact with the 3D avatar:
   - Left-click and drag to rotate
   - Scroll to zoom
   - Right-click and drag to pan
8. Use the morph slider to see transitions (if target was set)
9. Download the GLB file or take a screenshot

## Testing with Sample Data

Sample DEXA PDFs are available in `data/samples/`:
- `194_REES_Beau_.pdf`
- `196_ISMAIL_Nahla_.pdf`
- `205_GILDER_Bradley_.pdf`

Sample body photos are also available in the same directory.

## API Testing

You can test the API directly using curl:

```bash
# Parse a DEXA PDF
curl -X POST "http://localhost:8000/api/parse-dexa" \
  -F "file=@data/samples/194_REES_Beau_.pdf"

# Generate an avatar
curl -X POST "http://localhost:8000/api/generate-avatar" \
  -F "dexa_file=@data/samples/194_REES_Beau_.pdf"
```

## Troubleshooting

### Backend Issues

- **Import errors**: Make sure virtual environment is activated
- **Port already in use**: Change port with `--port 8001`
- **Missing dependencies**: Run `pip install -r requirements.txt` again

### Frontend Issues

- **Module not found**: Run `npm install` again
- **Port already in use**: Vite will automatically use the next available port
- **CORS errors**: Make sure backend is running and CORS is enabled

### GLB Loading Issues

- **Avatar not displaying**: Check browser console for errors
- **File not found**: Verify the avatar was generated in `output/` directory
- **Loading forever**: Check network tab to see if GLB file is being fetched

## Next Steps

- Integrate SMPL-X models for more accurate avatars
- Add face personalization (stretch goal)
- Enhance morphing with full mesh interpolation
- Add batch processing UI
- Implement screenshot functionality

