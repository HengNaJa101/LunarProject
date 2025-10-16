@echo off
echo ========================================
echo   Thai Lunar Calendar Server Launcher
echo ========================================

echo.
echo [1/4] กำลังไปยัง directory โปรเจค...
cd /d "%~dp0"

echo.
echo [2/4] กำลังเปิดใช้ virtual environment...
call .venv\Scripts\activate

echo.
echo [3/4] ตรวจสอบ dependencies...
python -c "import socket, json, threading; print('✓ Dependencies พร้อมใช้งาน')"

echo.
echo [4/4] เริ่มต้น Thai Lunar Calendar Server...
echo กำลังรันบน Port 5433...
echo กด Ctrl+C เพื่อหยุด server
echo.

python lunar_server.py

echo.
echo Server หยุดทำงานแล้ว
pause