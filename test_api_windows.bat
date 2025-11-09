@echo off
REM Test Thai Lunar Calendar API endpoints

echo Thai Lunar Calendar API Testing...
echo ====================================

echo.
echo 1. Testing Health Check:
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/health'; $response | ConvertTo-Json } catch { Write-Host 'Error: API not responding' }"

echo.
echo 2. Testing User Profile:
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/usersinfo/get/profile'; $response | ConvertTo-Json } catch { Write-Host 'Error: Profile endpoint failed' }"

echo.
echo 3. Testing Today Data:
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/lunar/today'; $response | ConvertTo-Json } catch { Write-Host 'Error: Today endpoint failed' }"

echo.
echo 4. Testing Date Query:
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/lunar/date/2025-11-09'; $response | ConvertTo-Json } catch { Write-Host 'Error: Date endpoint failed' }"

echo.
echo 5. Testing Stats:
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/lunar/stats'; $response | ConvertTo-Json } catch { Write-Host 'Error: Stats endpoint failed' }"

echo.
echo ====================================
echo Testing complete!
echo.
echo To access from other machines:
echo http://YOUR-SERVER-IP:8000/health
echo http://YOUR-SERVER-IP:8000/usersinfo/get/profile
pause