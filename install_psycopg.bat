@echo off
echo 🔧 Alternative installation using psycopg (newer version)...
echo.

echo Step 1: Update pip
python -m pip install --upgrade pip

echo.
echo Step 2: Uninstall old versions
pip uninstall psycopg2 psycopg2-binary psycopg -y

echo.
echo Step 3: Install psycopg with binary support
pip install "psycopg[binary]>=3.1.0"

echo.
echo Step 4: Install Flask
pip install Flask==2.3.3

echo.
echo Step 5: Test installation
python -c "import psycopg; print('✅ psycopg imported successfully')"
python -c "import flask; print('✅ Flask imported successfully')"

echo.
echo 🎉 Installation completed with psycopg (newer version)!
echo ⚠️  Note: You may need to update the connection code to use psycopg instead of psycopg2
pause