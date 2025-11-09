@echo off
echo 🔧 Installing Python packages for Windows Server...
echo.

echo Step 1: Update pip
python -m pip install --upgrade pip

echo.
echo Step 2: Uninstall old psycopg2 versions
pip uninstall psycopg2 psycopg2-binary -y

echo.
echo Step 3: Install psycopg2-binary (Windows compatible)
pip install psycopg2-binary==2.9.9

echo.
echo Step 4: Install Flask
pip install Flask==2.3.3

echo.
echo Step 5: Test installation
python -c "import psycopg2; print('✅ psycopg2 imported successfully')"
python -c "import flask; print('✅ Flask imported successfully')"

echo.
echo 🎉 Installation completed!
echo.
echo Next steps:
echo 1. Create database 'thai_lunar_db' in pgAdmin
echo 2. Run: python test_connection.py
echo 3. Start API: python api.py
pause