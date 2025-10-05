@echo off
echo ========================================
echo   LunarProject PM2 Deployment Script
echo ========================================

echo.
echo [1/10] Checking requirements...
node --version
npm --version
pm2 --version
python --version

echo.
echo [2/10] Going to C: drive...
C:
cd C:\

echo.
echo [3/10] Downloading LunarProject...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/HengNaJa101/LunarProject/archive/refs/heads/main.zip' -OutFile 'LunarProject.zip'"
powershell -Command "Expand-Archive -Path 'LunarProject.zip' -DestinationPath 'C:\' -Force"
powershell -Command "if (Test-Path 'C:\LunarProject') { Remove-Item 'C:\LunarProject' -Recurse -Force }"
powershell -Command "Rename-Item -Path 'C:\LunarProject-main' -NewName 'LunarProject'"
powershell -Command "Remove-Item 'LunarProject.zip'"

echo.
echo [4/10] Entering project directory...
cd C:\LunarProject

echo.
echo [5/10] Creating virtual environment...
python -m venv venv

echo.
echo [6/10] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [7/10] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [8/10] Creating logs directory...
if not exist "logs" mkdir logs

echo.
echo [9/10] Starting PM2...
pm2 delete lunar-project 2>nul
pm2 start ecosystem.config.js

echo.
echo [10/10] Checking status...
pm2 status
pm2 save

echo.
echo ========================================
echo   Deployment completed!
echo   Check logs with: pm2 logs lunar-project
echo ========================================
pause