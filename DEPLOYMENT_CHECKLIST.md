# Deployment Checklist

## Pre-Deployment

- [x] All code committed and pushed to GitHub
- [x] Vercel configuration file created (`frontend/vercel.json`)
- [x] Environment variable support added
- [x] Build configuration optimized
- [x] Documentation complete

## Frontend Deployment (Vercel)

### Step 1: Connect Repository
- [ ] Go to https://vercel.com
- [ ] Sign in with GitHub
- [ ] Click "New Project"
- [ ] Import `DEXA_3D_Scan` repository
- [ ] Set Root Directory to `frontend`

### Step 2: Configure Build
- [ ] Vercel should auto-detect Vite
- [ ] Verify build command: `npm run build`
- [ ] Verify output directory: `dist`

### Step 3: Set Environment Variables
- [ ] Add `VITE_API_URL` = Your backend URL (e.g., `https://your-backend.railway.app`)
- [ ] Do NOT include trailing slash

### Step 4: Deploy
- [ ] Click "Deploy"
- [ ] Wait for build to complete
- [ ] Test the deployed frontend

## Backend Deployment

### Option 1: Railway (Recommended)

1. **Create Account**
   - [ ] Sign up at https://railway.app
   - [ ] Connect GitHub account

2. **Create Project**
   - [ ] Click "New Project"
   - [ ] Select "Deploy from GitHub repo"
   - [ ] Select `DEXA_3D_Scan` repository
   - [ ] Set root directory to `backend`

3. **Configure**
   - [ ] Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - [ ] Add environment variables:
     - `OUTPUT_DIR` = `/app/output` (or default)
     - `SMPLX_MODEL_DIR` = `/app/models` (if using models)
     - `CORS_ORIGINS` = Your Vercel frontend URL

4. **Deploy**
   - [ ] Railway will auto-deploy
   - [ ] Get the generated URL
   - [ ] Update frontend `VITE_API_URL` in Vercel

### Option 2: Render

1. **Create Account**
   - [ ] Sign up at https://render.com
   - [ ] Connect GitHub

2. **Create Web Service**
   - [ ] New → Web Service
   - [ ] Connect `DEXA_3D_Scan` repository
   - [ ] Set root directory: `backend`
   - [ ] Build command: `pip install -r requirements.txt`
   - [ ] Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   - [ ] Add same variables as Railway

4. **Deploy**
   - [ ] Render will auto-deploy
   - [ ] Get URL and update frontend

## Post-Deployment Testing

- [ ] Test backend API: `https://your-backend.railway.app/docs`
- [ ] Test frontend: `https://your-project.vercel.app`
- [ ] Test DEXA PDF upload
- [ ] Test avatar generation
- [ ] Test 3D viewer
- [ ] Test screenshot functionality
- [ ] Verify CORS is working
- [ ] Test file downloads

## Troubleshooting

### Frontend Issues
- **Build fails**: Check Node.js version (need 18+)
- **API calls fail**: Verify `VITE_API_URL` is set correctly
- **CORS errors**: Check backend CORS configuration

### Backend Issues
- **Import errors**: Verify all dependencies in `requirements.txt`
- **Port issues**: Use `$PORT` environment variable
- **File upload fails**: Check file size limits
- **Model loading fails**: Verify model files are in correct location

## Next Steps After Deployment

1. **Monitor Logs**: Check Vercel and backend logs for errors
2. **Set Up Domain**: Configure custom domain if needed
3. **Add Analytics**: Optional - add usage tracking
4. **Performance**: Monitor and optimize as needed

