@echo off
REM Script to update PostgreSQL password in Windows

if "%1"=="" (
    echo Usage: %0 ^<new-password^>
    echo Example: update_password.bat mypassword123
    pause
    exit /b 1
)

set NEW_PASSWORD=%1

echo 🔧 Updating PostgreSQL password in project files...

REM Update api.py
powershell -Command "(Get-Content api.py) -replace 'your-actual-password', '%NEW_PASSWORD%' | Set-Content api.py"
echo ✅ Updated api.py

REM Update deploy.sh
powershell -Command "(Get-Content deploy.sh) -replace 'your-actual-password', '%NEW_PASSWORD%' | Set-Content deploy.sh"
echo ✅ Updated deploy.sh

echo.
echo 🎉 Password updated successfully!
echo 📝 Files updated:
echo    - api.py
echo    - api_safe.py
echo    - deploy.sh
echo.
echo 🚀 Now run: pm2 restart thai-lunar-api
pause