@echo off
echo กำลังรีสตาร์ททุกบริการ PM2...

pm2 restart all

echo.
echo สถานะปัจจุบัน:
pm2 status

echo.
echo ✅ รีสตาร์ททุกบริการเรียบร้อยแล้ว!
pause