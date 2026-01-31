# DOCX to PDF Converter

A production-ready web application to convert DOCX files to PDF format with single and bulk upload support.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

🚀 **[Live Demo](https://your-deployment-url.com)** | 📖 **[Deployment Guide](DEPLOYMENT.md)**

## Features

- 📤 Upload .doc and .docx files (single or bulk)
- 🔄 Convert to PDF instantly
- 💾 Download converted PDFs individually or as ZIP
- 📦 Bulk upload and convert multiple files at once
- 🎨 Clean and modern UI with mode toggle
- 📱 Responsive design
- 🚀 Drag and drop support
- 📊 Real-time conversion status for each file
- 🎯 Smart file validation and error handling

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Sharmaketann/convertDocToPdf.git
cd convertDocToPdf
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install LibreOffice:
```bash
# macOS
brew install --cask libreoffice

# Linux (Ubuntu/Debian)
sudo apt-get install libreoffice

# Windows - Download from https://www.libreoffice.org/
```

5. Copy environment file:
```bash
cp .env.example .env
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Choose between Single File or Bulk Upload mode

4. Upload DOCX file(s) and click "Convert to PDF"

5. Download converted PDFs individually or all as a ZIP file

## Usage Modes

### Single File Mode
- Upload and convert one file at a time
- Instant download after conversion
- Maximum file size: 16MB

### Bulk Upload Mode
- Upload multiple files simultaneously
- Convert all files in one click
- View conversion status for each file
- Download all converted files as a ZIP archive
- Maximum total size: 100MB

## System Requirements

- Python 3.7+
- Microsoft Word (required for docx2pdf on Windows)
- LibreOffice (alternative on Linux/Mac)

## Notes

- Single file mode: Maximum 16MB per file
- Bulk upload mode: Maximum 100MB total
- Supported formats: .doc, .docx
- Converted files are temporarily stored in the `converted` folder
- Uploaded files are automatically deleted after conversion
- Bulk download creates a ZIP file with all converted PDFs

## Troubleshooting

If you encounter issues with docx2pdf:

### On macOS:
```bash
brew install libreoffice
```

### On Linux:
```bash
sudo apt-get install libreoffice
```

### On Windows:
- Ensure Microsoft Word is installed, or
- Install LibreOffice from https://www.libreoffice.org/

## Project Structure

```
convertPdf/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
├── templates/         # HTML templates
│   └── index.html     # Main page
├── uploads/           # Temporary upload folder
└── converted/         # Converted PDF files
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy Options

#### Render (Recommended)
1. Fork this repository
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your repository
5. Render will auto-detect settings from `render.yaml`

#### Railway
```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

#### Docker
```bash
docker build -t docx-pdf-converter .
docker run -p 5000:5000 docx-pdf-converter
```

**⚠️ Note:** Vercel is not recommended due to serverless limitations. Use Render, Railway, or Heroku instead.

## API Documentation

### Endpoints

#### `GET /`
Main application interface

#### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "libreoffice_installed": true,
  "message": "Ready to convert"
}
```

#### `POST /upload`
Single file upload and conversion
- **Content-Type**: `multipart/form-data`
- **Body**: `file` - DOCX file
- **Response**:
```json
{
  "success": true,
  "message": "File converted successfully",
  "download_url": "/download/filename.pdf"
}
```

#### `POST /bulk-upload`
Multiple file upload and conversion
- **Content-Type**: `multipart/form-data`
- **Body**: `files[]` - Array of DOCX files
- **Response**:
```json
{
  "success": true,
  "converted": 5,
  "failed": 0,
  "results": [...],
  "errors": []
}
```

#### `GET /download/<filename>`
Download converted PDF file

#### `POST /download-all`
Download all converted files as ZIP
- **Content-Type**: `application/json`
- **Body**: `{"filenames": ["file1.pdf", "file2.pdf"]}`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security

- File validation (DOCX only)
- Size limits (16MB per file, 100MB bulk)
- Secure filename handling
- Temporary file cleanup
- CORS enabled

## Support

For issues and questions:
- Open an issue on GitHub
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help

## License

MIT License
