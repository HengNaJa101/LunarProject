@echo off
echo ======================================
echo   PostgreSQL Service Check for Server
echo ======================================
echo.

echo 1. ตรวจสอบ PostgreSQL Service...
sc query | findstr postgres
if errorlevel 1 (
    echo ❌ PostgreSQL Service ไม่พบ
) else (
    echo ✅ PostgreSQL Service พบแล้ว
)

echo.
echo 2. ตรวจสอบ Port 5432...
netstat -an | findstr :5432
if errorlevel 1 (
    echo ❌ Port 5432 ไม่เปิด
) else (
    echo ✅ Port 5432 เปิดอยู่
)

echo.
echo 3. ตรวจสอบ PostgreSQL Installation...
if exist "C:\Program Files\PostgreSQL\17\bin\psql.exe" (
    echo ✅ PostgreSQL 17 ติดตั้งแล้ว
) else if exist "C:\Program Files\PostgreSQL\16\bin\psql.exe" (
    echo ✅ PostgreSQL 16 ติดตั้งแล้ว
) else if exist "C:\Program Files\PostgreSQL\15\bin\psql.exe" (
    echo ✅ PostgreSQL 15 ติดตั้งแล้ว
) else (
    echo ❌ PostgreSQL ไม่ได้ติดตั้ง
    echo.
    echo 💡 แนะนำ: ติดตั้ง PostgreSQL ด้วยคำสั่ง
    echo    winget install PostgreSQL.PostgreSQL.17
)

echo.
echo 4. ตรวจสอบ psycopg2...
python -c "import psycopg2; print('✅ psycopg2 พร้อมใช้งาน')" 2>nul || echo "❌ psycopg2 ไม่พบ - ติดตั้งด้วย: pip install psycopg2"

echo.
pause