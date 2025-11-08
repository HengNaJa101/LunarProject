@echo off
echo กำลังหยุดทุกบริการ PM2...

pm2 stop all

echo.
echo สถานะปัจจุบัน:
pm2 status

echo.
echo ✅ หยุดทุกบริการเรียบร้อยแล้ว!
pause