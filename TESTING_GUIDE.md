# Testing & Verification Guide

This guide will help you verify that the DEXA to 3D Avatar pipeline works correctly.

## Prerequisites Check

Before testing, ensure you have:

1. **Python 3.10+** installed
2. **Node.js 18+** installed
3. **All dependencies installed** (see setup steps below)

## Step 1: Backend Setup & Verification

### Install Backend Dependencies

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Test Backend Server

```bash
# Start the server
uvicorn app.main:app --reload

# In another terminal, test the health endpoint
curl http://localhost:8000/

# Expected response:
# {"status":"ok","message":"DEXA to 3D Avatar API"}
```

### Test DEXA PDF Parsing

```bash
# Test with a sample PDF
curl -X POST "http://localhost:8000/api/parse-dexa" \
  -F "file=@../data/samples/194_REES_Beau_.pdf"

# Expected: JSON response with extracted DEXA metrics
# Check for fields like:
# - body_metrics.total_fat_percent
# - body_metrics.total_lean_mass_kg
# - regions (arms, legs, trunk, etc.)
```

**Verification Checklist:**
- [ ] Server starts without errors
- [ ] Health endpoint returns OK
- [ ] DEXA PDF parsing extracts at least some metrics
- [ ] No import errors in console

## Step 2: Frontend Setup & Verification

### Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Test Frontend Build

```bash
# Check if Vite can start
npm run dev

# Should see:
# VITE v5.x.x  ready in xxx ms
# ➜  Local:   http://localhost:3000/
```

**Verification Checklist:**
- [ ] `npm install` completes without errors
- [ ] `npm run dev` starts successfully
- [ ] Frontend loads at http://localhost:3000
- [ ] No console errors in browser

## Step 3: End-to-End Pipeline Test

### Test Full Avatar Generation

1. **Start Backend** (Terminal 1):
```bash
cd backend
.venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

2. **Start Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

3. **Open Browser**: Navigate to `http://localhost:3000`

4. **Upload DEXA PDF**:
   - Click "Choose File" under "DEXA Scan PDF"
   - Select `data/samples/194_REES_Beau_.pdf` (or any sample PDF)
   - Click "Generate Avatar"

5. **Verify Results**:
   - [ ] Loading spinner appears
   - [ ] Processing completes (5-10 seconds)
   - [ ] 3D avatar appears in viewer
   - [ ] No error messages displayed
   - [ ] Avatar can be rotated/zoomed

### Test with Body Photo (Optional)

1. Upload DEXA PDF as above
2. Upload a body photo (use sample images in `data/samples/`)
3. Click "Generate Avatar"
4. Verify avatar reflects photo-based adjustments

### Test Morphing (If Target Set)

1. Upload DEXA PDF
2. Enter a target body fat % (e.g., 20.0)
3. Generate avatar
4. Use the morph slider
5. Verify avatar changes (currently simplified scaling)

**Verification Checklist:**
- [ ] PDF upload works
- [ ] Avatar generation completes successfully
- [ ] GLB file is created in `output/` directory
- [ ] 3D viewer displays the avatar
- [ ] Orbit controls work (rotate, zoom, pan)
- [ ] Download GLB button works
- [ ] No errors in browser console
- [ ] No errors in backend console

## Step 4: API Endpoint Testing

### Test All Endpoints

```bash
# 1. Parse DEXA
curl -X POST "http://localhost:8000/api/parse-dexa" \
  -F "file=@data/samples/194_REES_Beau_.pdf"

# 2. Generate Avatar
curl -X POST "http://localhost:8000/api/generate-avatar" \
  -F "dexa_file=@data/samples/194_REES_Beau_.pdf" \
  -o response.json

# Check response.json for avatar_id and glb_path

# 3. Download GLB (use avatar_id from step 2)
curl -O "http://localhost:8000/api/avatar/{avatar_id}/glb"

# 4. Test Morphing (requires two avatar states)
# First, generate two avatars with different parameters
# Then create a morph request (see API docs)
```

## Step 5: Verify Output Files

### Check Generated Files

```bash
# After generating an avatar, check:
ls output/

# Should see:
# - {avatar_id}.glb  (3D model file)
# - {avatar_id}.json (parameters metadata)
```

### Verify GLB File

1. Download the GLB file
2. Try opening it in:
   - Three.js editor: https://threejs.org/editor/
   - Blender (import as GLTF)
   - Online GLB viewers

**Verification Checklist:**
- [ ] GLB files are created
- [ ] GLB files are valid (can be opened)
- [ ] JSON metadata files contain parameters
- [ ] Files are served correctly via `/output/` endpoint

## Step 6: Error Handling Tests

### Test Invalid Inputs

1. **Invalid PDF**:
   - Upload a non-PDF file
   - Expected: Error message displayed

2. **Empty Upload**:
   - Try to submit without file
   - Expected: Form validation prevents submission

3. **Corrupted PDF**:
   - Upload a corrupted PDF
   - Expected: Graceful error handling

4. **Large File**:
   - Upload a very large PDF (>10MB)
   - Expected: Either processes or shows appropriate error

## Step 7: Performance Verification

### Check Processing Times

1. Time the avatar generation:
   - Small PDF (<1MB): Should complete in <10 seconds
   - Medium PDF (1-5MB): Should complete in <30 seconds

2. Check frontend responsiveness:
   - UI should remain responsive during processing
   - Loading indicators should be visible

3. Check memory usage:
   - Backend shouldn't crash on multiple requests
   - Frontend shouldn't freeze

## Common Issues & Solutions

### Issue: Backend won't start

**Possible causes:**
- Missing dependencies: `pip install -r requirements.txt`
- Port 8000 in use: Change port with `--port 8001`
- Python version: Need Python 3.10+

**Solution:**
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Frontend can't connect to backend

**Possible causes:**
- Backend not running
- CORS issues
- Wrong API URL

**Solution:**
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Verify `vite.config.js` proxy settings

### Issue: Avatar not displaying

**Possible causes:**
- GLB file not generated
- GLB file path incorrect
- Three.js loading error

**Solution:**
- Check `output/` directory for GLB files
- Check browser console for loading errors
- Verify GLB file is accessible at `/output/{avatar_id}.glb`

### Issue: DEXA parsing fails

**Possible causes:**
- PDF format not supported
- PDF is scanned image (needs OCR)
- Regex patterns don't match PDF format

**Solution:**
- Check if PDF has selectable text (not scanned)
- Review extracted text in parser
- May need to adjust regex patterns for your PDF format

## Automated Testing (Future)

For production, consider adding:

1. **Unit Tests**:
   - Test DEXA parser with known PDFs
   - Test parameter mapping functions
   - Test morphing interpolation

2. **Integration Tests**:
   - Test full API endpoints
   - Test file upload/download
   - Test error handling

3. **E2E Tests**:
   - Test full user workflow
   - Test UI interactions
   - Test 3D viewer functionality

## Success Criteria

Your pipeline is working correctly if:

✅ Backend starts without errors
✅ Frontend loads and connects to backend
✅ DEXA PDFs can be uploaded and parsed
✅ Avatars are generated and saved as GLB files
✅ 3D viewer displays avatars correctly
✅ Orbit controls work smoothly
✅ Download functionality works
✅ No critical errors in console
✅ Processing completes in reasonable time (<30s)

## Next Steps After Verification

Once verified, you can:

1. **Test with real DEXA scans** from your use case
2. **Integrate SMPL-X models** for realistic avatars
3. **Enhance morphing** with full mesh interpolation
4. **Add face personalization** (stretch goal)
5. **Optimize performance** for production use

