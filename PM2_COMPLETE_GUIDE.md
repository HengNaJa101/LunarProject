# 🚀 PM2 Command Center - LunarProject
## คู่มือและเครื่องมือครบครันสำหรับจัดการ PM2 บน Windows Server

---

## 📋 สารบัญ
1. [คำสั่งพื้นฐาน PM2](#คำสั่งพื้นฐาน-pm2)
2. [การรันแอปพลิเคชัน](#การรันแอปพลิเคชัน)
3. [การจัดการ Process](#การจัดการ-process)
4. [Monitoring และ Logs](#monitoring-และ-logs)
5. [Startup Management](#startup-management)
6. [คำสั่งสำหรับ LunarProjectNew](#คำสั่งสำหรับ-lunarprojectnew)
7. [Interactive Menu Script](#interactive-menu-script)
8. [Batch Scripts Collection](#batch-scripts-collection)
9. [Server Setup Guide](#server-setup-guide)
10. [Troubleshooting](#troubleshooting)

---

## 📋 คำสั่งพื้นฐาน PM2

### ติดตั้ง PM2
```cmd
npm install -g pm2
pm2 --version
```

### ตรวจสอบสถานะ PM2
```cmd
pm2 status
pm2 list
pm2 ps
```

---

## 🚀 การรันแอปพลิเคชัน

### 1. รัน Lunar Project หลัก (ecosystem.config.js)
```cmd
pm2 start ecosystem.config.js
pm2 start ecosystem.config.js --env production
```

### 2. รัน Lunar Server (ecosystem-server.config.js)
```cmd
pm2 start ecosystem-server.config.js
```

### 3. รัน Interactive Mode (ecosystem-interactive.config.js)
```cmd
pm2 start ecosystem-interactive.config.js
```

### 4. รันทุกบริการ (ecosystem-full.config.js)
```cmd
pm2 start ecosystem-full.config.js
```

### 5. รันแบบระบุชื่อ App
```cmd
pm2 start FinishLunar.py --name "lunar-project" --interpreter python
pm2 start lunar_server.py --name "lunar-server" --interpreter python
pm2 start web_api.py --name "lunar-web-api" --interpreter python
pm2 start interactive_lunar.py --name "lunar-interactive" --interpreter python
```

---

## 🔧 การจัดการ Process

### หยุด Process
```cmd
pm2 stop all
pm2 stop lunar-project
pm2 stop lunar-server
pm2 stop lunar-interactive
pm2 stop lunar-web-api
pm2 stop 0
```

### รีสตาร์ท Process
```cmd
pm2 restart all
pm2 restart lunar-project
pm2 restart lunar-server
pm2 restart lunar-interactive
pm2 restart lunar-web-api
pm2 restart 0
```

### ลบ Process
```cmd
pm2 delete all
pm2 delete lunar-project
pm2 delete lunar-server
pm2 delete lunar-interactive
pm2 delete lunar-web-api
pm2 delete 0
```

### รีโหลด Process (Zero Downtime)
```cmd
pm2 reload all
pm2 reload lunar-project
```

---

## 📊 Monitoring และ Logs

### ดู Logs แบบ Real-time
```cmd
pm2 logs
pm2 logs lunar-project
pm2 logs lunar-server
pm2 logs --lines 100
pm2 logs --follow
```

### ดู Monitoring
```cmd
pm2 monit
pm2 info lunar-project
pm2 describe lunar-project
```

### ดูสถิติการใช้งาน
```cmd
pm2 show lunar-project
pm2 env 0
```

---

## 💾 Startup Management

### บันทึก Process List ปัจจุบัน
```cmd
pm2 save
```

### ตั้งค่าให้เริ่มต้นอัตโนมัติเมื่อ Boot
```cmd
pm2 startup
pm2 startup windows
```

### ลบการตั้งค่า Startup
```cmd
pm2 unstartup
```

### กู้คืน Process ที่บันทึกไว้
```cmd
pm2 resurrect
```

---

## 🎯 คำสั่งสำหรับ LunarProjectNew

### เข้าไปยังโปรเจ็กต์และรัน PM2:
```cmd
cd C:\LunarProjectNew
pm2 start ecosystem-full.config.js
```

### ดูสถานะ:
```cmd
cd C:\LunarProjectNew
pm2 status
```

### ดู Logs:
```cmd
cd C:\LunarProjectNew
pm2 logs
```

### หยุดทุกบริการ:
```cmd
cd C:\LunarProjectNew
pm2 stop all
```

### รีสตาร์ททุกบริการ:
```cmd
cd C:\LunarProjectNew
pm2 restart all
```

### อัปเดตโปรเจ็กต์จาก GitHub:
```cmd
cd C:\LunarProjectNew
git pull origin main
```

---

## 🎛️ Interactive Menu Script

สร้างไฟล์ `pm2_manager.bat` พร้อมเนื้อหา:

```batch
@echo off
echo ========================================
echo        PM2 Lunar Project Manager
echo ========================================
echo.

:menu
echo เลือกคำสั่งที่ต้องการ:
echo.
echo 1. เริ่มทุกบริการ (Full Services)
echo 2. เริ่มเฉพาะ Lunar Service
echo 3. เริ่มเฉพาะ Server
echo 4. เริ่มแบบ Interactive
echo 5. ดูสถานะทั้งหมด
echo 6. ดู Logs แบบ Real-time
echo 7. หยุดทุกบริการ
echo 8. รีสตาร์ททุกบริการ
echo 9. ลบทุก Process
echo 10. ตรวจสอบ Port
echo 11. บันทึกสถานะ PM2
echo 12. กู้คืน Process
echo 0. ออกจากโปรแกรม
echo.

set /p choice="กรุณาเลือก (0-12): "

if "%choice%"=="1" goto start_full
if "%choice%"=="2" goto start_service
if "%choice%"=="3" goto start_server
if "%choice%"=="4" goto start_interactive
if "%choice%"=="5" goto status
if "%choice%"=="6" goto logs
if "%choice%"=="7" goto stop_all
if "%choice%"=="8" goto restart_all
if "%choice%"=="9" goto delete_all
if "%choice%"=="10" goto check_ports
if "%choice%"=="11" goto save_pm2
if "%choice%"=="12" goto resurrect
if "%choice%"=="0" goto exit

echo ตัวเลือกไม่ถูกต้อง กรุณาลองใหม่
echo.
goto menu

:start_full
echo เริ่มทุกบริการ...
cd /d "C:\LunarProjectNew"
pm2 start ecosystem-full.config.js
pm2 status
pause
goto menu

:start_service
echo เริ่ม Lunar Service...
cd /d "C:\LunarProjectNew"
pm2 start ecosystem.config.js
pm2 status
pause
goto menu

:start_server
echo เริ่ม Lunar Server...
cd /d "C:\LunarProjectNew"
pm2 start ecosystem-server.config.js
pm2 status
pause
goto menu

:start_interactive
echo เริ่ม Interactive Mode...
cd /d "C:\LunarProjectNew"
pm2 start ecosystem-interactive.config.js
pm2 status
pause
goto menu

:status
echo สถานะ PM2:
pm2 status
pause
goto menu

:logs
echo กำลังแสดง Logs (กด Ctrl+C เพื่อหยุด)...
pm2 logs
pause
goto menu

:stop_all
echo หยุดทุกบริการ...
pm2 stop all
pm2 status
pause
goto menu

:restart_all
echo รีสตาร์ททุกบริการ...
pm2 restart all
pm2 status
pause
goto menu

:delete_all
echo ลบทุก Process...
set /p confirm="ยืนยันการลบ? (y/n): "
if /i "%confirm%"=="y" (
    pm2 delete all
    pm2 status
)
pause
goto menu

:check_ports
echo ตรวจสอบ Port...
cd /d "C:\LunarProjectNew"
if exist check_ports.bat (
    call check_ports.bat
) else (
    echo กำลังตรวจสอบ Port 5433 และ 8000...
    netstat -an | findstr :5433
    netstat -an | findstr :8000
)
pause
goto menu

:save_pm2
echo บันทึกสถานะ PM2...
pm2 save
echo สถานะได้รับการบันทึกแล้ว
pause
goto menu

:resurrect
echo กู้คืน Process...
pm2 resurrect
pm2 status
pause
goto menu

:exit
echo ออกจากโปรแกรม...
exit /b 0
```

---

## 📱 Batch Scripts Collection

### 1. start_all_services.bat
```batch
@echo off
echo กำลังเริ่มทุกบริการ Lunar Project...
cd /d "C:\LunarProjectNew"

echo ตรวจสอบ PM2...
pm2 --version >nul 2>&1
if errorlevel 1 (
    echo Error: PM2 ไม่ได้ติดตั้ง กรุณาติดตั้ง PM2 ก่อน
    echo npm install -g pm2
    pause
    exit /b 1
)

echo เริ่มทุกบริการจาก ecosystem-full.config.js...
pm2 start ecosystem-full.config.js

echo.
echo สถานะปัจจุบัน:
pm2 status

echo.
echo บันทึกสถานะ PM2...
pm2 save

echo.
echo ✅ เริ่มทุกบริการเรียบร้อยแล้ว!
echo.
echo คำสั่งที่มีประโยชน์:
echo - ดูสถานะ: pm2 status
echo - ดู logs: pm2 logs
echo - หยุดทุกอย่าง: pm2 stop all
echo - รีสตาร์ท: pm2 restart all
echo.
pause
```

### 2. stop_all_services.bat
```batch
@echo off
echo กำลังหยุดทุกบริการ PM2...

pm2 stop all

echo.
echo สถานะปัจจุบัน:
pm2 status

echo.
echo ✅ หยุดทุกบริการเรียบร้อยแล้ว!
pause
```

### 3. restart_all_services.bat
```batch
@echo off
echo กำลังรีสตาร์ททุกบริการ PM2...

pm2 restart all

echo.
echo สถานะปัจจุบัน:
pm2 status

echo.
echo ✅ รีสตาร์ททุกบริการเรียบร้อยแล้ว!
pause
```

### 4. show_status.bat
```batch
@echo off
echo แสดงสถานะ PM2...
echo.

pm2 status

echo.
echo รายละเอียดเพิ่มเติม:
echo - ดู logs: pm2 logs
echo - ดู monitoring: pm2 monit
echo - ดูรายละเอียด app: pm2 show [app-name]
echo.
pause
```

### 5. show_logs.bat
```batch
@echo off
echo แสดง Logs แบบ Real-time...
echo กด Ctrl+C เพื่อหยุด

pm2 logs
```

---

## 🆕 Server Setup Guide

### การตั้งค่าใหม่บน Server:

#### วิธีที่ 1: Clone ใหม่ (แนะนำ)
```cmd
cd C:\
mkdir LunarProjectNew
cd LunarProjectNew
git clone https://github.com/HengNaJa101/LunarProject.git .
```

#### วิธีที่ 2: อัปเดตจากที่มีอยู่
```cmd
cd C:\LunarProjectNew
git pull origin main
```

### การตั้งค่า Python Environment:
```cmd
cd C:\LunarProjectNew
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### ตั้งค่า PM2 Auto-start:
```cmd
pm2 startup windows
pm2 save
```

---

## 🛠️ Troubleshooting

### แก้ไขปัญหาที่พบบ่อย:

#### 1. PM2 ไม่พบคำสั่ง:
```cmd
npm install -g pm2
```

#### 2. Python Environment ไม่ถูกต้อง:
แก้ไขในไฟล์ `ecosystem-full.config.js`:
```javascript
interpreter: 'C:\\LunarProjectNew\\.venv\\Scripts\\python.exe'
cwd: 'C:\\LunarProjectNew'
```

#### 3. Port ถูกใช้งานแล้ว:
```cmd
netstat -an | findstr :5433
netstat -an | findstr :8000
taskkill /F /PID [PID_NUMBER]
```

#### 4. หยุดทุก Process และเริ่มใหม่:
```cmd
pm2 kill
pm2 start ecosystem-full.config.js
```

#### 5. ตรวจสอบ PM2 Daemon:
```cmd
pm2 ping
pm2 kill
pm2 resurrect
```

---

## 🎯 คำสั่งที่ใช้บ่อย

```cmd
# เริ่มทุกอย่าง
pm2 start ecosystem-full.config.js

# ดูสถานะ
pm2 status

# ดู logs
pm2 logs

# หยุดทุกอย่าง
pm2 stop all

# รีสตาร์ททุกอย่าง
pm2 restart all

# บันทึกสถานะ
pm2 save

# อัปเดตโปรเจ็กต์
git pull origin main
```

---

## ⚡ Quick Reference

| คำสั่ง | ความหมาย |
|--------|-----------|
| `pm2 status` | ดูสถานะทั้งหมด |
| `pm2 logs` | ดู logs แบบ real-time |
| `pm2 monit` | เปิด monitoring dashboard |
| `pm2 restart all` | รีสตาร์ททุก process |
| `pm2 stop all` | หยุดทุก process |
| `pm2 delete all` | ลบทุก process |
| `pm2 save` | บันทึก process list |
| `pm2 resurrect` | กู้คืน process ที่บันทึก |

---

## 📞 สนับสนุน

หากมีปัญหาการใช้งาน:
1. ตรวจสอบ logs: `pm2 logs`
2. ดูสถานะ: `pm2 status` 
3. ตรวจสอบ Python environment
4. ตรวจสอบ port conflicts
5. อ่าน error logs ใน `./logs/` folder

---

**✅ ไฟล์นี้รวมทุกอย่างที่ต้องการสำหรับจัดการ PM2 บน LunarProject!**