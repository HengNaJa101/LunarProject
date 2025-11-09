@echo off
echo 🔧 Update Server IP Configuration
echo.

if "%1"=="" (
    echo Usage: %0 ^<SERVER_IP^>
    echo Example: %0 192.168.1.100
    echo.
    echo Current configuration:
    echo.
    type server_config.py | findstr "SERVER_IP"
    echo.
    pause
    exit /b 1
)

set NEW_IP=%1

echo Updating server IP to: %NEW_IP%
echo.

REM Update server_config.py
powershell -Command "(Get-Content server_config.py) -replace 'SERVER_IP = \".*\"', 'SERVER_IP = \"%NEW_IP%\"' | Set-Content server_config.py"

echo ✅ Updated server_config.py
echo.

echo Testing connection...
python server_config.py

echo.
echo 🎉 Configuration updated!
echo You can now run: python api.py
pause