@echo off
echo ========================================
echo        PM2 Lunar Project Manager
echo ========================================
echo.

:menu
echo เลือกคำสั่งที่ต้องการ:
echo.
echo 1. เริ่มทุกบริการ (Full Services)
echo 2. เริ่มเฉพาะ Lunar Service
echo 3. เริ่มเฉพาะ Server
echo 4. เริ่มแบบ Interactive
echo 5. ดูสถานะทั้งหมด
echo 6. ดู Logs แบบ Real-time
echo 7. หยุดทุกบริการ
echo 8. รีสตาร์ททุกบริการ
echo 9. ลบทุก Process
echo 10. ตรวจสอบ Port
echo 11. บันทึกสถานะ PM2
echo 12. กู้คืน Process
echo 0. ออกจากโปรแกรม
echo.

set /p choice="กรุณาเลือก (0-12): "

if "%choice%"=="1" goto start_full
if "%choice%"=="2" goto start_service
if "%choice%"=="3" goto start_server
if "%choice%"=="4" goto start_interactive
if "%choice%"=="5" goto status
if "%choice%"=="6" goto logs
if "%choice%"=="7" goto stop_all
if "%choice%"=="8" goto restart_all
if "%choice%"=="9" goto delete_all
if "%choice%"=="10" goto check_ports
if "%choice%"=="11" goto save_pm2
if "%choice%"=="12" goto resurrect
if "%choice%"=="0" goto exit

echo ตัวเลือกไม่ถูกต้อง กรุณาลองใหม่
echo.
goto menu

:start_full
echo เริ่มทุกบริการ...
cd /d "C:\Users\User 2\LunarProject"
pm2 start ecosystem-full.config.js
pm2 status
pause
goto menu

:start_service
echo เริ่ม Lunar Service...
cd /d "C:\Users\User 2\LunarProject"
pm2 start ecosystem.config.js
pm2 status
pause
goto menu

:start_server
echo เริ่ม Lunar Server...
cd /d "C:\Users\User 2\LunarProject"
pm2 start ecosystem-server.config.js
pm2 status
pause
goto menu

:start_interactive
echo เริ่ม Interactive Mode...
cd /d "C:\Users\User 2\LunarProject"
pm2 start ecosystem-interactive.config.js
pm2 status
pause
goto menu

:status
echo สถานะ PM2:
pm2 status
pause
goto menu

:logs
echo กำลังแสดง Logs (กด Ctrl+C เพื่อหยุด)...
pm2 logs
pause
goto menu

:stop_all
echo หยุดทุกบริการ...
pm2 stop all
pm2 status
pause
goto menu

:restart_all
echo รีสตาร์ททุกบริการ...
pm2 restart all
pm2 status
pause
goto menu

:delete_all
echo ลบทุก Process...
set /p confirm="ยืนยันการลบ? (y/n): "
if /i "%confirm%"=="y" (
    pm2 delete all
    pm2 status
)
pause
goto menu

:check_ports
echo ตรวจสอบ Port...
cd /d "C:\Users\User 2\LunarProject"
if exist check_ports.bat (
    call check_ports.bat
) else (
    echo กำลังตรวจสอบ Port 5433 และ 8000...
    netstat -an | findstr :5433
    netstat -an | findstr :8000
)
pause
goto menu

:save_pm2
echo บันทึกสถานะ PM2...
pm2 save
echo สถานะได้รับการบันทึกแล้ว
pause
goto menu

:resurrect
echo กู้คืน Process...
pm2 resurrect
pm2 status
pause
goto menu

:exit
echo ออกจากโปรแกรม...
exit /b 0