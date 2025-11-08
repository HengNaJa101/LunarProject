@echo off
echo กำลังเริ่มทุกบริการ Lunar Project...
cd /d "C:\Users\User 2\LunarProject"

echo ตรวจสอบ PM2...
pm2 --version >nul 2>&1
if errorlevel 1 (
    echo Error: PM2 ไม่ได้ติดตั้ง กรุณาติดตั้ง PM2 ก่อน
    echo npm install -g pm2
    pause
    exit /b 1
)

echo เริ่มทุกบริการจาก ecosystem-full.config.js...
pm2 start ecosystem-full.config.js

echo.
echo สถานะปัจจุบัน:
pm2 status

echo.
echo บันทึกสถานะ PM2...
pm2 save

echo.
echo ✅ เริ่มทุกบริการเรียบร้อยแล้ว!
echo.
echo คำสั่งที่มีประโยชน์:
echo - ดูสถานะ: pm2 status
echo - ดู logs: pm2 logs
echo - หยุดทุกอย่าง: pm2 stop all
echo - รีสตาร์ท: pm2 restart all
echo.
pause