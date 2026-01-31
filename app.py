from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import tempfile
import uuid
import zipfile
from io import BytesIO
import shutil
import logging
import subprocess
import platform
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_level = logging.DEBUG if os.getenv('FLASK_ENV') == 'development' else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration from environment or defaults
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['CONVERTED_FOLDER'] = os.getenv('CONVERTED_FOLDER', 'converted')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
CONVERTED_FOLDER = app.config['CONVERTED_FOLDER']
ALLOWED_EXTENSIONS = {'doc', 'docx'}

# Create necessary folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Check if LibreOffice is installed
def check_libreoffice():
    """Check if LibreOffice/soffice is available"""
    return shutil.which('soffice') is not None or shutil.which('libreoffice') is not None

def convert_docx_to_pdf(input_path, output_path):
    """Convert DOCX to PDF using LibreOffice directly on macOS"""
    try:
        if platform.system() == 'Darwin':  # macOS
            # Use LibreOffice command line directly
            soffice_path = shutil.which('soffice')
            if not soffice_path:
                raise Exception("LibreOffice not found. Please install: brew install --cask libreoffice")

            # Get output directory
            output_dir = os.path.dirname(output_path)

            # Run LibreOffice conversion
            cmd = [
                soffice_path,
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', output_dir,
                input_path
            ]

            logger.debug(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode != 0:
                logger.error(f"LibreOffice error: {result.stderr}")
                raise Exception(f"Conversion failed: {result.stderr}")

            # LibreOffice creates the file with the original name, we need to rename it
            input_filename = os.path.basename(input_path)
            temp_output = os.path.join(output_dir, input_filename.rsplit('.', 1)[0] + '.pdf')

            if os.path.exists(temp_output) and temp_output != output_path:
                os.rename(temp_output, output_path)

            logger.debug(f"Conversion successful: {output_path}")
        else:
            # Use docx2pdf for Windows/Linux
            from docx2pdf import convert
            convert(input_path, output_path)

    except subprocess.TimeoutExpired:
        raise Exception("Conversion timed out. File may be too large or complex.")

@app.before_request
def check_dependencies():
    """Check dependencies before first request"""
    if not hasattr(app, 'dependencies_checked'):
        if not check_libreoffice():
            logger.warning("LibreOffice not found. Conversion may fail.")
        app.dependencies_checked = True


def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    libreoffice_installed = check_libreoffice()
    return jsonify({
        'status': 'healthy' if libreoffice_installed else 'degraded',
        'libreoffice_installed': libreoffice_installed,
        'message': 'Ready to convert' if libreoffice_installed else 'LibreOffice not found. Install with: brew install --cask libreoffice'
    })


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and conversion"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .doc and .docx files are allowed'}), 400

        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}_{original_filename}"

        # Save uploaded file
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        logger.debug(f"Saved file to: {input_path}")

        # Generate output PDF path
        pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
        output_path = os.path.join(app.config['CONVERTED_FOLDER'], pdf_filename)
        logger.debug(f"Converting to: {output_path}")

        # Convert to PDF
        convert_docx_to_pdf(input_path, output_path)

        # Verify conversion succeeded
        if not os.path.exists(output_path):
            raise Exception("Conversion failed. PDF file was not created.")

        logger.debug(f"Conversion successful: {output_path}")

        # Clean up uploaded file
        os.remove(input_path)

        return jsonify({
            'success': True,
            'message': 'File converted successfully',
            'download_url': f'/download/{pdf_filename}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/bulk-upload', methods=['POST'])
def bulk_upload():
    """Handle multiple file uploads and conversions"""
    try:
        # Check if files are present
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('files[]')

        if not files or len(files) == 0:
            return jsonify({'error': 'No files selected'}), 400

        results = []
        errors = []

        for file in files:
            if file.filename == '':
                continue

            # Check if file type is allowed
            if not allowed_file(file.filename):
                errors.append({
                    'filename': file.filename,
                    'error': 'Invalid file type'
                })
                continue

            try:
                # Generate unique filename
                original_filename = secure_filename(file.filename)
                unique_id = str(uuid.uuid4())
                filename = f"{unique_id}_{original_filename}"

                # Save uploaded file
                input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(input_path)
                logger.debug(f"Saved file to: {input_path}")

                # Generate output PDF path
                pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
                output_path = os.path.join(app.config['CONVERTED_FOLDER'], pdf_filename)
                logger.debug(f"Converting to: {output_path}")

                # Convert to PDF
                convert_docx_to_pdf(input_path, output_path)

                # Verify conversion succeeded
                if not os.path.exists(output_path):
                    raise Exception("Conversion failed. PDF file was not created.")

                logger.debug(f"Conversion successful: {output_path}")

                # Clean up uploaded file
                os.remove(input_path)

                results.append({
                    'original_filename': original_filename,
                    'pdf_filename': pdf_filename,
                    'download_url': f'/download/{pdf_filename}',
                    'success': True
                })

            except Exception as e:
                errors.append({
                    'filename': file.filename,
                    'error': str(e)
                })

        return jsonify({
            'success': True,
            'converted': len(results),
            'failed': len(errors),
            'results': results,
            'errors': errors
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download the converted PDF file"""
    try:
        file_path = os.path.join(app.config['CONVERTED_FOLDER'], filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        # Get original filename without unique ID
        original_name = '_'.join(filename.split('_')[1:])

        return send_file(
            file_path,
            as_attachment=True,
            download_name=original_name,
            mimetype='application/pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download-all', methods=['POST'])
def download_all():
    """Download all converted files as a ZIP"""
    try:
        data = request.get_json()
        filenames = data.get('filenames', [])

        if not filenames:
            return jsonify({'error': 'No files to download'}), 400

        # Create a BytesIO object to store the ZIP file in memory
        memory_file = BytesIO()

        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in filenames:
                file_path = os.path.join(app.config['CONVERTED_FOLDER'], filename)

                if os.path.exists(file_path):
                    # Get original filename without unique ID
                    original_name = '_'.join(filename.split('_')[1:])
                    zipf.write(file_path, original_name)

        memory_file.seek(0)

        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name='converted_pdfs.zip'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Development server
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
