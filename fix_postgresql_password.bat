@echo off
echo ===============================================
echo   PostgreSQL Password Reset for Server
echo ===============================================
echo.

echo 1. Checking PostgreSQL service...
sc query postgresql-x64-16
if errorlevel 1 (
    echo ❌ PostgreSQL 16 service not found
    echo Try: sc query postgresql-x64-17
    pause
    exit /b 1
)

echo.
echo 2. Testing current connection...
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -c "SELECT 1;" 2>nul
if %errorLevel% == 0 (
    echo ✅ PostgreSQL connection works!
    goto :test_python
)

echo.
echo 3. Setting PostgreSQL password...
echo Method 1: Using psql (may require existing password)
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -c "ALTER USER postgres PASSWORD 'postgres';"

if %errorLevel__ == 0 (
    echo ✅ Password set successfully!
    goto :test_python
)

echo.
echo Method 2: Edit pg_hba.conf (temporary trust)
echo Location: C:\Program Files\PostgreSQL\16\data\pg_hba.conf
echo Change "md5" to "trust" for local connections
echo Then restart PostgreSQL service and run this script again

echo.
echo Method 3: Windows Authentication
echo PostgreSQL might be configured for Windows auth only

:test_python
echo.
echo 4. Testing Python connection...
cd /d "C:\LunarProjectNew"
python -c "import psycopg2; conn = psycopg2.connect(host='localhost', port=5432, database='postgres', user='postgres', password='postgres'); print('✅ Python connection successful!'); conn.close()" 2>nul

if %errorLevel% == 0 (
    echo ✅ Ready to run migration!
) else (
    echo ❌ Python connection failed
    echo Try different passwords or configuration
)

echo.
pause