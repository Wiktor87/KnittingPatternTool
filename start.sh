#!/bin/bash
# Knitting Pattern Tool Startup Script

echo "=========================================="
echo "  🧶 Knitting Pattern Tool Startup 🧶"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher from python.org"
    exit 1
fi

echo "✓ Python 3 found"

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing/updating dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting Knitting Pattern Tool..."
echo "=========================================="
echo "The application will open in your browser at:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the application"
echo "=========================================="
echo ""

# Start the Flask application
python app.py
