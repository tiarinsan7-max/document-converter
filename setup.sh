#!/bin/bash

# Universal Document Converter - Setup Script
# This script sets up the virtual environment and installs dependencies

set -e  # Exit on error

echo "🚀 Setting up Universal Document Converter..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate the virtual environment:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Try a conversion:"
echo "      python main.py convert input.pdf output.docx"
echo ""
echo "   3. Start the API server:"
echo "      python main.py api"
echo ""
echo "   4. Start Streamlit UI:"
echo "      python main.py streamlit"
echo ""
echo "   5. View supported formats:"
echo "      python main.py formats"
echo ""
echo "🎉 Happy converting!"
