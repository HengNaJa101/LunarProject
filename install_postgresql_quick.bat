@echo off
echo ===============================================
echo   PostgreSQL Installation for Server
echo ===============================================
echo.

echo 1. ตรวจสอบสิทธิ์ Administrator...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Administrator privileges confirmed
) else (
    echo ❌ Need Administrator privileges
    echo Please run as Administrator
    pause
    exit /b 1
)

echo.
echo 2. Installing PostgreSQL 17...
winget install PostgreSQL.PostgreSQL.17 --accept-package-agreements --accept-source-agreements

echo.
echo 3. Starting PostgreSQL service...
timeout /t 5 /nobreak
sc start postgresql-x64-17

echo.
echo 4. Setting PostgreSQL password...
echo Please set password for postgres user when prompted
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -c "ALTER USER postgres PASSWORD 'postgres';"

echo.
echo 5. Testing connection...
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -c "SELECT version();"

echo.
echo ===============================================
echo ✅ PostgreSQL installation completed!
echo Next steps:
echo 1. Run: python migrate_to_postgresql.py
echo 2. Run: pm2 restart all
echo ===============================================
pause