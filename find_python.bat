@echo off
REM Script to find Python path and run PM2

echo 🔍 Finding Python installation...

REM ตรวจสอบ Python commands ที่เป็นไปได้
where python >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Found: python
    python --version
    echo.
    echo 🚀 Starting PM2 with python...
    pm2 start pm2.config.js
    goto :end
)

where python3 >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Found: python3
    python3 --version
    echo.
    echo 🚀 Starting PM2 with python3...
    pm2 start pm2.config.js
    goto :end
)

where py >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Found: py launcher
    py --version
    echo.
    echo 🚀 Starting PM2 with py launcher...
    pm2 start api.py --name thai-lunar-api --interpreter py
    goto :end
)

REM ถ้าไม่เจอ Python ให้แสดง path ที่เป็นไปได้
echo ❌ Python not found in PATH
echo.
echo 🔧 Please check these locations:
dir "C:\Python*" 2>nul
dir "C:\Program Files\Python*" 2>nul
dir "C:\Users\%USERNAME%\AppData\Local\Programs\Python*" 2>nul
echo.
echo 💡 Solutions:
echo 1. Add Python to PATH environment variable
echo 2. Use full path in pm2-windows.config.js
echo 3. Install Python from python.org

:end
pause