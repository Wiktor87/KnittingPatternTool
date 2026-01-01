@echo off
REM Knitting Pattern Tool Startup Script for Windows

echo ==========================================
echo   🧶 Knitting Pattern Tool Startup 🧶
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo ✓ Python found

REM Check if virtual environment exists, create if not
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing/updating dependencies...
pip install -q -r requirements.txt

echo.
echo Starting Knitting Pattern Tool...
echo ==========================================
echo The application will open in your browser at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the application
echo ==========================================
echo.

REM Start the Flask application
python app.py

pause
