@echo off
echo แสดงสถานะ PM2...
echo.

pm2 status

echo.
echo รายละเอียดเพิ่มเติม:
echo - ดู logs: pm2 logs
echo - ดู monitoring: pm2 monit
echo - ดูรายละเอียด app: pm2 show [app-name]
echo.
pause