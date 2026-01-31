# Deployment Guide

This guide covers deploying the DOCX to PDF Converter to various platforms.

## ⚠️ Important: Vercel Limitations

**Vercel is NOT recommended for this application** because:
- Vercel uses serverless functions with limited execution time
- LibreOffice cannot be installed in Vercel's serverless environment
- File system access is restricted

### Recommended Platforms Instead:
- **Render** (Recommended) - Free tier available, supports LibreOffice
- **Railway** - Easy deployment, supports LibreOffice
- **Fly.io** - Global deployment, full control
- **Heroku** - Classic PaaS, supports buildpacks
- **DigitalOcean App Platform** - Easy deployment

---

## Deployment Options

### 1. Render (Recommended)

**Why Render?**
- Free tier available
- Automatic LibreOffice support
- Easy deployment from GitHub
- Auto-deploy on git push

**Steps:**

1. Push code to GitHub (see below)
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `docx-to-pdf-converter`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

6. Add environment variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key-here
   ```

7. Click "Create Web Service"

**Install LibreOffice on Render:**

Add this to a `render.yaml` file (or use Shell commands in dashboard):

```yaml
services:
  - type: web
    name: docx-pdf-converter
    env: python
    buildCommand: |
      pip install -r requirements.txt
      apt-get update
      apt-get install -y libreoffice
    startCommand: gunicorn app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
```

---

### 2. Railway

**Steps:**

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login and deploy:
   ```bash
   railway login
   railway init
   railway up
   ```

3. Add LibreOffice buildpack:
   - Go to Railway dashboard
   - Select your project
   - Add buildpack: `https://github.com/heroku/heroku-buildpack-apt`
   - Create `Aptfile` with content: `libreoffice`

---

### 3. Heroku

**Steps:**

1. Install Heroku CLI:
   ```bash
   brew install heroku/brew/heroku  # macOS
   ```

2. Login and create app:
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. Add LibreOffice buildpack:
   ```bash
   heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
   ```

4. Create `Aptfile`:
   ```
   libreoffice
   ```

5. Deploy:
   ```bash
   git push heroku main
   ```

---

### 4. Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

# Install LibreOffice
RUN apt-get update && apt-get install -y \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create necessary directories
RUN mkdir -p uploads converted

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
```

**Build and run:**

```bash
docker build -t docx-pdf-converter .
docker run -p 5000:5000 docx-pdf-converter
```

---

## Environment Variables

Set these environment variables in your deployment platform:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment (development/production) | development | No |
| `SECRET_KEY` | Secret key for Flask sessions | Random | **Yes** (production) |
| `PORT` | Port to run the server | 5000 | No |
| `MAX_CONTENT_LENGTH` | Max upload size in bytes | 104857600 (100MB) | No |
| `UPLOAD_FOLDER` | Folder for temporary uploads | uploads | No |
| `CONVERTED_FOLDER` | Folder for converted files | converted | No |

---

## Post-Deployment Checklist

- [ ] Verify LibreOffice is installed (`/health` endpoint)
- [ ] Test single file conversion
- [ ] Test bulk file conversion
- [ ] Test download all as ZIP
- [ ] Check application logs
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Configure custom domain (optional)
- [ ] Set up SSL certificate (most platforms auto-configure)

---

## Monitoring & Maintenance

### Health Check Endpoint

Use `/health` to monitor application status:

```bash
curl https://your-app.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "libreoffice_installed": true,
  "message": "Ready to convert"
}
```

### Logs

Monitor application logs for errors:

**Render:**
```bash
# View logs in dashboard or CLI
render logs
```

**Railway:**
```bash
railway logs
```

**Heroku:**
```bash
heroku logs --tail
```

---

## Troubleshooting

### LibreOffice Not Found

**Error:** "LibreOffice not found"

**Solution:**
1. Verify LibreOffice installation on the platform
2. Check `/health` endpoint
3. Review deployment logs
4. Ensure buildpack/apt packages are installed

### Conversion Timeout

**Error:** "Conversion timed out"

**Solution:**
1. Increase worker timeout in `Procfile`:
   ```
   web: gunicorn app:app --timeout 180
   ```
2. Check file size limits
3. Verify LibreOffice is functioning

### File Not Found After Conversion

**Error:** "File not found" on download

**Solution:**
1. Check file system permissions
2. Verify `converted` folder exists
3. Check application logs for conversion errors

---

## Scaling Considerations

For high-traffic deployments:

1. **Increase Workers:**
   ```
   web: gunicorn app:app --workers 8 --timeout 120
   ```

2. **Use Redis for Session Storage:**
   - Add `redis` and `flask-session` to requirements
   - Configure Flask-Session

3. **Add File Cleanup:**
   - Implement periodic cleanup of old files
   - Use cron job or scheduled task

4. **CDN for Static Assets:**
   - Serve templates/static files via CDN
   - Use object storage for converted files

---

## Security Best Practices

- [ ] Set strong `SECRET_KEY` in production
- [ ] Enable HTTPS (auto on most platforms)
- [ ] Implement rate limiting
- [ ] Add file size validation
- [ ] Scan uploaded files for malware
- [ ] Set up CORS properly
- [ ] Implement user authentication (if needed)
- [ ] Regular security updates

---

## Cost Estimation

**Free Tiers:**
- Render: 750 hours/month
- Railway: $5 free credit/month
- Heroku: Limited free tier (with sleep)

**Paid Plans:**
- Render: Starting at $7/month
- Railway: Pay as you go
- Heroku: Starting at $7/month

**Recommendation:** Start with Render's free tier, upgrade as needed.
