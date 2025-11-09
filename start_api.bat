@echo off
REM Alternative ways to start Thai Lunar API

echo 🌙 Thai Lunar API - Alternative Startup Methods
echo ================================================

echo 📋 Method 1: Try different Python commands
echo.

REM Method 1: ลอง python
echo Trying: python api.py
python api.py 2>nul
if %errorlevel% == 0 goto :success

REM Method 2: ลอง python3  
echo Trying: python3 api.py
python3 api.py 2>nul
if %errorlevel% == 0 goto :success

REM Method 3: ลอง py launcher
echo Trying: py api.py
py api.py 2>nul
if %errorlevel% == 0 goto :success

echo.
echo ❌ Could not start with direct Python commands
echo.
echo 📋 Method 2: PM2 with full path
echo.

REM PM2 Method 1: ลอง python
echo Trying PM2 with python...
pm2 start api.py --name thai-lunar-api --interpreter python
if %errorlevel% == 0 goto :pm2success

REM PM2 Method 2: ลอง py launcher
echo Trying PM2 with py launcher...
pm2 start api.py --name thai-lunar-api --interpreter py
if %errorlevel% == 0 goto :pm2success

REM PM2 Method 3: ใช้ config file แก้ไขแล้ว
echo Trying PM2 with config...
pm2 start pm2.config.js
if %errorlevel% == 0 goto :pm2success

echo.
echo ❌ All methods failed. Please check:
echo 1. Python is installed
echo 2. Python is in PATH
echo 3. Required packages are installed: pip install Flask psycopg2-binary
echo.
goto :end

:success
echo ✅ API started successfully with direct Python!
echo 🌐 Access: http://localhost:8000/health
goto :end

:pm2success
echo ✅ API started successfully with PM2!
echo 🌐 Access: http://localhost:8000/health
echo 📊 Check status: pm2 status
echo 📋 View logs: pm2 logs thai-lunar-api

:end
pause