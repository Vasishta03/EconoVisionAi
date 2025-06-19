@echo off
echo 🌍 EconoVisionAI Windows Launcher
echo =====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Install dependencies if needed
if not exist venv (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies ready

REM Launch application
echo 🚀 Starting EconoVisionAI...
python main.py

if errorlevel 1 (
    echo ❌ Application failed to start
    pause
    exit /b 1
)

echo 👋 Application closed
pause
