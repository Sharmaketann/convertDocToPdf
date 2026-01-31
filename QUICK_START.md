# 🚀 Quick Start Guide

## ✅ Code Successfully Pushed to GitHub!

Your code is now live at: **https://github.com/Sharmaketann/convertDocToPdf**

---

## ⚠️ Important: About Vercel

**Vercel WILL NOT WORK** for this application because:
- LibreOffice cannot run in Vercel's serverless environment
- File conversion requires a full Linux environment
- Execution timeouts will kill conversions

**📖 See [VERCEL_WARNING.md](VERCEL_WARNING.md) for details**

---

## ✅ Recommended: Deploy to Render (FREE)

### Why Render?
- ✅ **Free tier** (750 hours/month)
- ✅ **LibreOffice works** perfectly
- ✅ **One-click deploy** from GitHub
- ✅ **Auto-installs** everything you need
- ✅ **5-minute setup**

### Steps to Deploy:

1. **Go to Render:**
   👉 https://render.com

2. **Sign up** with your GitHub account

3. **Create new Web Service:**
   - Click "New +" → "Web Service"
   - Select repository: `convertDocToPdf`
   - Click "Connect"

4. **Configure (auto-detected):**
   - Name: `docx-pdf-converter`
   - Environment: `Python 3`
   - Build Command: Auto-detected from `render.yaml`
   - Start Command: Auto-detected

5. **Add Environment Variables:**
   - `SECRET_KEY`: Generate a random string
   - `FLASK_ENV`: `production`
   (Or let Render auto-generate from `render.yaml`)

6. **Click "Create Web Service"**

7. **Wait 5-10 minutes** for:
   - Installing Python packages
   - Installing LibreOffice
   - Building the application
   - Starting the server

8. **Your app is live!** 🎉
   - You'll get a URL like: `https://docx-pdf-converter.onrender.com`
   - Health check: `https://your-url.onrender.com/health`

---

## 📦 What's Included

### Production Features:
- ✅ Single file upload & conversion
- ✅ Bulk upload & conversion
- ✅ Download as individual PDFs
- ✅ Download all as ZIP
- ✅ Modern responsive UI
- ✅ Real-time conversion status
- ✅ Health check endpoint
- ✅ CORS enabled
- ✅ Environment variable config
- ✅ Production-ready logging

### Deployment Files:
- ✅ `render.yaml` - Render one-click deploy
- ✅ `Procfile` - Heroku/Railway
- ✅ `Aptfile` - LibreOffice installation
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version
- ✅ `.env.example` - Environment variables template
- ✅ `DEPLOYMENT.md` - Comprehensive deployment guide

---

## 🧪 Test Your Deployment

Once deployed, test these endpoints:

1. **Health Check:**
   ```bash
   curl https://your-app.onrender.com/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "libreoffice_installed": true,
     "message": "Ready to convert"
   }
   ```

2. **Upload a file via UI:**
   - Visit your app URL
   - Upload a DOCX file
   - Click "Convert to PDF"
   - Download the PDF

3. **Test bulk upload:**
   - Switch to "Bulk Upload" mode
   - Upload multiple DOCX files
   - Convert all at once
   - Download as ZIP

---

## 📊 Platform Comparison

| Feature | Vercel | Render | Railway |
|---------|--------|--------|---------|
| Works with LibreOffice | ❌ No | ✅ Yes | ✅ Yes |
| Free Tier | ✅ Yes | ✅ Yes | $5 credit |
| Setup Time | N/A | 5 min | 5 min |
| Auto-deploy | ✅ Yes | ✅ Yes | ✅ Yes |
| Custom domains | ✅ Yes | ✅ Yes | ✅ Yes |
| **Recommended** | ❌ | ✅ | ✅ |

---

## 🔗 Important Links

- **GitHub Repository:** https://github.com/Sharmaketann/convertDocToPdf
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Vercel Warning:** [VERCEL_WARNING.md](VERCEL_WARNING.md)
- **Render Dashboard:** https://dashboard.render.com

---

## 🆘 Troubleshooting

### LibreOffice not found
**Solution:** Render should auto-install from `render.yaml`. Check build logs.

### Conversion timeout
**Solution:** Increase timeout in `Procfile`:
```
web: gunicorn app:app --timeout 180
```

### Files not persisting
**Solution:** This is normal. Converted files are temporary and cleaned up after download.

---

## 🎯 Next Steps

1. ✅ Deploy to Render (recommended)
2. ✅ Test all features
3. ✅ Set up custom domain (optional)
4. ✅ Monitor with health checks
5. ✅ Add error tracking (Sentry, etc.)

---

## 💡 Pro Tips

- **Auto-deploys:** Render auto-deploys when you push to `main` branch
- **Environment vars:** Set in Render dashboard under "Environment"
- **Logs:** View real-time logs in Render dashboard
- **Scale:** Upgrade to paid plan for better performance
- **Custom domain:** Add your domain in Render settings

---

## 🤝 Support

Need help?
- 📖 Check [DEPLOYMENT.md](DEPLOYMENT.md)
- 🐛 Open an issue on GitHub
- 💬 Review existing issues

---

**Ready to deploy? Go to [render.com](https://render.com) now!**
