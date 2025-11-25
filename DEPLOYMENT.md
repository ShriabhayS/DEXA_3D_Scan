# Deployment Guide

## Frontend Deployment on Vercel

### Prerequisites
- Vercel account (free tier works)
- GitHub repository connected

### Steps

1. **Install Vercel CLI** (optional, for local testing):
```bash
npm i -g vercel
```

2. **Deploy via Vercel Dashboard**:
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Select `frontend` as the root directory
   - Vercel will auto-detect Vite/React

3. **Set Environment Variables**:
   - In Vercel project settings, add:
   - `VITE_API_URL` = Your backend API URL (e.g., `https://your-backend.railway.app`)

4. **Deploy**:
   - Vercel will automatically build and deploy
   - Your frontend will be live at `https://your-project.vercel.app`

## Backend Deployment Options

Vercel supports serverless functions, but for a full FastAPI app, consider:

### Option 1: Railway (Recommended)
- Free tier available
- Easy Python deployment
- Automatic HTTPS

### Option 2: Render
- Free tier available
- Good for FastAPI
- Easy setup

### Option 3: Heroku
- Paid plans available
- Well-documented
- Easy deployment

### Option 4: Vercel Serverless Functions
- Convert FastAPI to serverless functions
- More complex setup
- Better for API-only endpoints

## Environment Variables for Backend

Set these in your backend hosting platform:
- `SMPLX_MODEL_DIR` - Path to SMPL-X models (if using)
- `OUTPUT_DIR` - Directory for generated files
- `CORS_ORIGINS` - Allowed frontend origins

## Full Stack Deployment

1. Deploy backend first (Railway/Render/Heroku)
2. Get backend URL
3. Set `VITE_API_URL` in Vercel frontend deployment
4. Update `vercel.json` rewrites if needed

## Testing Deployment

1. Test backend API: `https://your-backend.railway.app/docs`
2. Test frontend: `https://your-project.vercel.app`
3. Verify API calls work from frontend
4. Test file uploads and downloads

