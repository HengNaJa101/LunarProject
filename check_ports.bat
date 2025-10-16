@echo off
echo ========================================
echo   Port and Database Checker
echo ========================================

echo.
echo [1] Checking PostgreSQL Port (5432)...
netstat -an | findstr :5432
if %ERRORLEVEL% == 0 (
    echo ✅ PostgreSQL is running on port 5432
) else (
    echo ❌ PostgreSQL not found on port 5432
)

echo.
echo [2] Checking our server port (5433)...
netstat -an | findstr :5433
if %ERRORLEVEL% == 0 (
    echo ✅ Thai Lunar Server is running on port 5433
) else (
    echo ℹ️ Port 5433 is available for our server
)

echo.
echo [3] Checking all LISTENING ports...
echo Active ports:
netstat -an | findstr LISTEN

echo.
echo [4] Testing database connections...
cd /d "%~dp0"
call .venv\Scripts\activate
python database_config.py

echo.
echo [5] PostgreSQL Service Status...
sc query postgresql*
if %ERRORLEVEL% == 0 (
    echo ✅ PostgreSQL service found
) else (
    echo ❌ PostgreSQL service not found
)

echo.
pause