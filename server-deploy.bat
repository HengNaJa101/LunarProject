@echo off
echo ========================================
echo   LunarProject PM2 Deployment Script
echo ========================================

echo.
echo [1/12] Checking requirements...
node --version
npm --version
pm2 --version
python --version

echo.
echo [2/12] Going to project directory...
cd %~dp0

echo.
echo [3/12] Checking if virtual environment exists...
if exist "venv" (
    echo Virtual environment found.
) else (
    echo [4/12] Creating virtual environment...
    python -m venv venv
)

echo.
echo [5/12] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [6/12] Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
pip install psycopg2-binary --only-binary=psycopg2-binary

echo.
echo [7/12] Creating logs directory...
if not exist "logs" mkdir logs

echo.
echo [8/12] Checking ecosystem.config.js...
if exist "ecosystem.config.js" (
    echo Configuration file found.
) else (
    echo ERROR: ecosystem.config.js not found!
    pause
    exit /b 1
)

echo.
echo [9/12] Stopping existing PM2 processes...
pm2 delete lunar-project 2>nul

echo.
echo [10/12] Starting PM2 with new configuration...
pm2 start ecosystem.config.js

echo.
echo [11/12] Checking PM2 status...
pm2 status

echo.
echo [12/12] Saving PM2 configuration...
pm2 save

echo.
echo ========================================
echo   Deployment completed successfully!
echo ========================================
echo.
echo Useful commands:
echo   pm2 status              - Check status
echo   pm2 logs lunar-project  - View logs  
echo   pm2 restart lunar-project - Restart service
echo   pm2 monit              - Monitor resources
echo.
pause