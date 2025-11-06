# Netlify Deployment Guide

## 🚀 Deploy to Netlify

### Method 1: Deploy via Netlify UI (Recommended)

1. **Sign up/Login to Netlify**
   - Go to: https://app.netlify.com
   - Sign up or login with GitHub

2. **Connect Repository**
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub
   - Select repository: `awaleayush777/sunspots_predictor_2.0`
   - Branch: `main`

3. **Configure Build Settings**
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `.` (root)
   - Functions directory: `netlify/functions`
   - Python version: `3.11`

4. **Deploy**
   - Click "Deploy site"
   - Wait for build to complete
   - Your site will be live at: `https://your-site-name.netlify.app`

### Method 2: Deploy via Netlify CLI

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```
   Or using winget:
   ```bash
   winget install Netlify.CLI
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Initialize Site**
   ```bash
   cd "C:\sun spot 2.0"
   netlify init
   ```
   - Choose "Create & configure a new site"
   - Follow the prompts

4. **Deploy**
   ```bash
   netlify deploy --prod
   ```

### Method 3: Deploy via GitHub Integration

1. **Push to GitHub** (Already done ✅)
   - Your code is already on GitHub

2. **Connect on Netlify**
   - Go to Netlify dashboard
   - Click "Add new site" → "Import an existing project"
   - Select your GitHub repository
   - Netlify will auto-detect settings from `netlify.toml`

3. **Automatic Deploys**
   - Every push to `main` branch will auto-deploy
   - Pull requests will create preview deployments

## 📋 Configuration Files

### `netlify.toml`
- Build configuration
- Function settings
- Redirect rules

### `runtime.txt`
- Python version specification
- Required for Netlify to use correct Python version

### `netlify/functions/app.py`
- Serverless function wrapper
- Handles Flask app routing

## 🔧 Build Settings

**Build Command:**
```bash
pip install -r requirements.txt
```

**Publish Directory:**
```
. (root directory)
```

**Functions Directory:**
```
netlify/functions
```

**Python Version:**
```
3.11
```

## ⚙️ Environment Variables (Optional)

If needed, add in Netlify dashboard:
- `FLASK_ENV=production`
- `PYTHON_VERSION=3.11`

## 🐛 Troubleshooting

### Build Fails

1. **Check build logs** in Netlify dashboard
2. **Verify Python version** matches `runtime.txt`
3. **Check dependencies** in `requirements.txt`
4. **Verify function path** is correct

### Function Timeout

- Netlify Functions have a 10-second timeout (free tier)
- For longer operations, consider optimizing the model loading
- Or upgrade to Pro plan for longer timeouts

### Import Errors

- Make sure all dependencies are in `requirements.txt`
- Check that paths are correct in `netlify/functions/app.py`

## 📊 Monitoring

- **Deploy logs**: Available in Netlify dashboard
- **Function logs**: Check "Functions" tab
- **Analytics**: Available in Netlify dashboard (Pro plan)

## 🔄 Continuous Deployment

Once connected to GitHub:
- ✅ Every push to `main` = Production deploy
- ✅ Pull requests = Preview deploy
- ✅ Automatic rollback on failed builds

## 🌐 Custom Domain

1. Go to Site settings → Domain management
2. Add custom domain
3. Follow DNS configuration instructions
4. SSL certificate is automatic

## 📝 Notes

- Netlify Functions run in a serverless environment
- Cold starts may occur (first request after inactivity)
- Consider caching model if needed
- Free tier includes 125,000 function invocations/month

## 🎯 Next Steps

1. Deploy to Netlify using one of the methods above
2. Test your deployed site
3. Set up custom domain (optional)
4. Configure environment variables if needed
5. Monitor function usage

---

**Status**: ✅ Ready to deploy! Configuration files are in place.

