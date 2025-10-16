@echo off
echo ========================================
echo   Thai Lunar Calendar Server Launcher
echo ========================================

echo.
echo [1/4] Navigating to project directory...
cd /d "%~dp0"

echo.
echo [2/4] Activating virtual environment...
call .venv\Scripts\activate

echo.
echo [3/4] Checking dependencies...
python -c "import socket, json, threading; print('✓ Dependencies ready')"

echo.
echo [4/4] Starting Thai Lunar Calendar Server...
echo Running on Port 5433...
echo Press Ctrl+C to stop server
echo.

python lunar_server.py

echo.
echo Server stopped
pause