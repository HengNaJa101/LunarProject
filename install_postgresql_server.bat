@echo off
echo ===============================================
echo   PostgreSQL Installation Script for Server
echo ===============================================
echo.

echo กำลังตรวจสอบสิทธิ์ Administrator...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ มีสิทธิ์ Administrator
) else (
    echo ❌ ต้องรันด้วยสิทธิ์ Administrator
    echo กรุณาคลิกขวาที่ Command Prompt และเลือก "Run as administrator"
    pause
    exit /b 1
)

echo.
echo 1. ตรวจสอบ winget...
winget --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ winget พร้อมใช้งาน
) else (
    echo ❌ winget ไม่พบ
    echo กรุณาอัปเดต Windows หรือติดตั้ง App Installer จาก Microsoft Store
    pause
    exit /b 1
)

echo.
echo 2. ค้นหา PostgreSQL...
winget search PostgreSQL.PostgreSQL.17

echo.
echo 3. ติดตั้ง PostgreSQL 17...
echo กำลังดาวน์โหลดและติดตั้ง... (อาจใช้เวลาสักครู่)
winget install PostgreSQL.PostgreSQL.17 --accept-package-agreements --accept-source-agreements

if %errorLevel__ == 0 (
    echo ✅ ติดตั้ง PostgreSQL สำเร็จ
) else (
    echo ❌ ติดตั้งล้มเหลว
    echo ลองติดตั้งด้วยตัวเอง: https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)

echo.
echo 4. รอให้ service เริ่มทำงาน...
timeout /t 10 /nobreak

echo.
echo 5. ตรวจสอบ PostgreSQL Service...
sc query postgresql-x64-17
if %errorLevel% == 0 (
    echo ✅ PostgreSQL Service รันอยู่
) else (
    echo ⚠️ กำลังเริ่ม PostgreSQL Service...
    sc start postgresql-x64-17
)

echo.
echo 6. ตรวจสอบ Port 5432...
netstat -an | findstr :5432

echo.
echo ===============================================
echo ✅ การติดตั้งเสร็จสิ้น!
echo.
echo ขั้นตอนต่อไป:
echo 1. ตั้งรหัสผ่านสำหรับ user postgres
echo 2. รัน: python smart_database_setup.py
echo 3. รัน: pm2 start ecosystem-full.config.js
echo ===============================================
pause