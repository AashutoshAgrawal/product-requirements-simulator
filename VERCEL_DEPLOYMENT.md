# Vercel Deployment Guide

## Issues Found & Fixed

### 1. ✅ Missing vercel.json Configuration
**Problem**: No Vercel configuration file for React app in subdirectory
**Solution**: Created `/vercel.json` with proper build settings

### 2. ✅ Duplicate Entry Point Files
**Problem**: Both `index.js` and `index.tsx` existed, causing potential conflicts
**Solution**: Removed `index.js` since the app uses TypeScript

### 3. ⚠️ Build Warnings (Non-Critical)
**Issue**: Unused imports and CSS calc warnings
**Impact**: Build succeeds but with warnings - won't prevent deployment

## Deployment Steps

### Option 1: Deploy from Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**: https://vercel.com/new

2. **Import Your Repository**:
   - Click "Import Project"
   - Select your GitHub repository: `AashutoshAgrawal/product-requirements-simulator`
   - Click "Import"

3. **Configure Project Settings**:
   ```
   Framework Preset: Create React App
   Root Directory: ./
   Build Command: cd react-frontend && npm install && npm run build
   Output Directory: react-frontend/build
   Install Command: (leave default)
   ```

4. **Environment Variables**:
   Add the following environment variable:
   ```
   Name: REACT_APP_API_URL
   Value: https://elicitron-backend.onrender.com
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes for build completion
   - Your app will be live at: `https://your-project-name.vercel.app`

### Option 2: Deploy from CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project root
cd /Users/aashutosh/product-requirements-simulator
vercel --prod

# Follow prompts:
# - Set up and deploy? Yes
# - Scope: Select your account
# - Link to existing project? No
# - Project name: product-requirements-simulator
# - Directory: ./
# - Override settings? Yes
#   - Build Command: cd react-frontend && npm install && npm run build
#   - Output Directory: react-frontend/build
#   - Install Command: npm install (default)
```

## Post-Deployment

### Update Environment Variable
If your backend URL changes, update it in Vercel:
1. Go to your project in Vercel Dashboard
2. Settings → Environment Variables
3. Edit `REACT_APP_API_URL`
4. Redeploy (automatic on next git push, or click "Redeploy" in Deployments tab)

### Verify Deployment

Test your deployed app:
```bash
# Check if site loads
curl -I https://your-project-name.vercel.app

# Test API connection (from browser console)
fetch('https://your-project-name.vercel.app')
  .then(r => r.text())
  .then(console.log)
```

## Troubleshooting

### Build Fails on Vercel

**Error**: "Module not found" or TypeScript errors
**Solution**: 
```bash
# Test build locally first
cd react-frontend
npm install
npm run build
```

### App Loads But API Calls Fail

**Issue**: CORS or wrong API URL
**Check**:
1. Verify `REACT_APP_API_URL` is set correctly in Vercel
2. Check browser console for errors
3. Ensure backend allows CORS from Vercel domain

**Fix Backend CORS** (in app_fastapi.py):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-project-name.vercel.app",
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variable Not Working

**Issue**: `process.env.REACT_APP_API_URL` is undefined
**Solution**: Environment variables must start with `REACT_APP_` for Create React App
- ✅ Correct: `REACT_APP_API_URL`
- ❌ Wrong: `API_URL`, `VITE_API_URL`, `NEXT_PUBLIC_API_URL`

After adding/changing env vars, you MUST redeploy (not just rebuild)

## Files Created/Modified

- ✅ `/vercel.json` - Vercel configuration
- ✅ `/.vercelignore` - Exclude unnecessary files from deployment
- ✅ Removed `/react-frontend/src/index.js` - Eliminated duplicate entry point
- ✅ `/VERCEL_DEPLOYMENT.md` - This guide

## Next Steps

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Add Vercel configuration and fix deployment issues"
   git push origin main
   ```

2. Deploy to Vercel using Option 1 or Option 2 above

3. Test your live app!

## Common Commands

```bash
# Redeploy to production
vercel --prod

# Deploy preview (test deployment)
vercel

# View deployment logs
vercel logs [deployment-url]

# List all deployments
vercel ls

# Remove a deployment
vercel rm [deployment-url]
```

## Additional Resources

- [Vercel Create React App Deployment](https://vercel.com/docs/frameworks/create-react-app)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Environment Variables](https://vercel.com/docs/environment-variables)
