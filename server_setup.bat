@echo off
REM Thai Lunar Calendar API - Complete Windows Server Setup Commands
REM รันไฟล์นี้บน Windows Server หรือคัดลอกคำสั่งไปรันทีละบรรทัด

echo 🚀 Starting Thai Lunar Calendar API Server Setup...

REM ========================================
REM 1. UPDATE REPOSITORY และ DEPENDENCIES
REM ========================================

echo 📦 Step 1: Update repository and install dependencies

REM ไปยัง directory โปรเจค (แก้ไข path ให้ถูกต้อง)
cd /d C:\path\to\LunarProject

REM ดึงโค้ดล่าสุดจาก GitHub
git pull origin main

REM ติดตั้ง Python packages ที่จำเป็น
pip install Flask psycopg2-binary

echo ✅ Repository updated and dependencies installed

REM ========================================
REM 2. TEST POSTGRESQL CONNECTION
REM ========================================

echo 🔗 Step 2: Testing PostgreSQL connection

python -c "import psycopg2; conn = psycopg2.connect(host='localhost', port=5432, database='thai_lunar_db', user='postgres', password='123456'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM lunar_calendar'); count = cursor.fetchone()[0]; print(f'✅ PostgreSQL OK - Found {count} records'); cursor.close(); conn.close()" || (echo ❌ PostgreSQL connection failed & exit /b 1)

REM ========================================
REM 3. CONFIGURE WINDOWS FIREWALL
REM ========================================

echo ⚙️ Step 3: Configure Windows Firewall

REM เปิดพอร์ต 8000 สำหรับ API
netsh advfirewall firewall add rule name="Thai Lunar API Port 8000" dir=in action=allow protocol=TCP localport=8000
echo ✅ Port 8000 opened in Windows Firewall

REM สร้าง logs directory
if not exist logs mkdir logs

REM ========================================
REM 4. START API WITH PM2
REM ========================================

echo 🚀 Step 4: Starting API with PM2

REM หยุด process เก่า (ถ้ามี)
pm2 stop thai-lunar-api 2>nul
pm2 delete thai-lunar-api 2>nul

REM เริ่ม API ด้วย PM2
pm2 start ecosystem-api-server.config.js --env production

REM บันทึก configuration
pm2 save

REM แสดงสถานะ
pm2 status

echo ✅ API started with PM2

REM ========================================
REM 4. TEST API ENDPOINTS
REM ========================================

echo 🧪 Step 4: Testing API endpoints

REM รอ API เริ่มต้น
timeout /t 3 /nobreak >nul

echo Testing /health endpoint:
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/health' | ConvertTo-Json"

echo Testing /usersinfo/get/profile endpoint:
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/usersinfo/get/profile' | ConvertTo-Json"

echo Testing /lunar/today endpoint:
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/lunar/today' | ConvertTo-Json"

echo Testing /lunar/date/2024-11-08 endpoint:
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/lunar/date/2024-11-08' | ConvertTo-Json"

echo Testing /lunar/stats endpoint:
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/lunar/stats' | ConvertTo-Json"

REM ========================================
REM 5. SETUP AUTO-START
REM ========================================

echo ⚙️ Step 5: Setup auto-start on boot

REM ตั้งค่า PM2 auto-start
pm2 startup

echo ✅ Auto-start configured

REM ========================================
REM 6. SHOW FINAL STATUS
REM ========================================

echo 📋 Final Status:
pm2 status
pm2 logs thai-lunar-api --lines 10

echo.
echo 🎉 Thai Lunar Calendar API Setup Complete!
echo.
echo 📊 API Endpoints:
echo    Health Check: http://localhost:8000/health
echo    User Profile: http://localhost:8000/usersinfo/get/profile
echo    Today Data:   http://localhost:8000/lunar/today
echo    Date Query:   http://localhost:8000/lunar/date/YYYY-MM-DD
echo    Statistics:   http://localhost:8000/lunar/stats
echo.
echo 🔧 Management Commands:
echo    pm2 status                    - ดูสถานะ
echo    pm2 logs thai-lunar-api       - ดู logs
echo    pm2 restart thai-lunar-api    - รีสตาร์ท
echo    pm2 stop thai-lunar-api       - หยุด
echo.

pause