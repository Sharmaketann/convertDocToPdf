#!/bin/bash

echo "🚀 Setting up DOCX to PDF Converter..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the app: python app.py"
echo "  3. Open http://localhost:5000 in your browser"
echo ""
echo "Note: On macOS/Linux, you may need to install LibreOffice:"
echo "  macOS: brew install libreoffice"
echo "  Linux: sudo apt-get install libreoffice"
