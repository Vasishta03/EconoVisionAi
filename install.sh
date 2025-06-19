#!/bin/bash
# Installation script for EconoVisionAI

echo "🌍 Installing EconoVisionAI Dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "📍 Python version: $python_version"

# Install requirements
echo "📦 Installing required packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Installation completed successfully!"
    echo ""
    echo "🚀 To run EconoVisionAI:"
    echo "   python3 main.py"
    echo ""
    echo "📁 Make sure you have data files in the 'data/' folder"
    echo "📄 and report files in the 'reports/' folder"
else
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi
