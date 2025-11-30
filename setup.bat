@echo off
REM Universal Document Converter - Setup Script for Windows
REM This script sets up the virtual environment and installs dependencies

echo 🚀 Setting up Universal Document Converter...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo    1. Activate the virtual environment:
echo       venv\Scripts\activate
echo.
echo    2. Try a conversion:
echo       python main.py convert input.pdf output.docx
echo.
echo    3. Start the API server:
echo       python main.py api
echo.
echo    4. Start Streamlit UI:
echo       python main.py streamlit
echo.
echo    5. View supported formats:
echo       python main.py formats
echo.
echo 🎉 Happy converting!
pause
