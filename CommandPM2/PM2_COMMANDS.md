# คำสั่ง PM2 สำหรับ Windows Server

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

## 📊 การตรวจสอบและ Monitoring

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

## 💾 การจัดการ Startup

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

## 🔄 การอัปเดตและ Maintenance

### อัปเดต PM2
```cmd
npm update -g pm2
pm2 update
```

### ล้าง Logs
```cmd
pm2 flush
pm2 flush lunar-project
```

### รีเซ็ต Restart Counter
```cmd
pm2 reset all
pm2 reset lunar-project
```

## 📁 คำสั่งสำหรับโปรเจ็กต์นี้โดยเฉพาะ

### รันเฉพาะ Lunar Service
```cmd
cd "C:\Users\User 2\LunarProject"
pm2 start ecosystem.config.js
```

### รันเฉพาะ Server
```cmd
cd "C:\Users\User 2\LunarProject"
pm2 start ecosystem-server.config.js
```

### รันทั้ง Service และ Interactive
```cmd
cd "C:\Users\User 2\LunarProject"
pm2 start ecosystem-interactive.config.js
```

### รันทุกบริการพร้อมกัน
```cmd
cd "C:\Users\User 2\LunarProject"
pm2 start ecosystem-full.config.js
```

### ตรวจสอบ Port ก่อนรัน
```cmd
cd "C:\Users\User 2\LunarProject"
check_ports.bat
```

## 🛠️ คำสั่งแก้ไขปัญหา

### หยุดทุก Process และเริ่มใหม่
```cmd
pm2 kill
pm2 start ecosystem-full.config.js
```

### ตรวจสอบ PM2 Daemon
```cmd
pm2 ping
pm2 kill
pm2 resurrect
```

### ดู Error Logs
```cmd
pm2 logs --err
pm2 logs lunar-project --err
```

### ดู Memory Usage
```cmd
pm2 show lunar-project
```

## 📱 คำสั่งแบบ Batch สำหรับ Windows

### สร้างไฟล์ .bat สำหรับรันง่าย ๆ

**start_all.bat:**
```batch
@echo off
cd /d "C:\Users\User 2\LunarProject"
pm2 start ecosystem-full.config.js
pm2 status
pause
```

**stop_all.bat:**
```batch
@echo off
pm2 stop all
pm2 status
pause
```

**restart_all.bat:**
```batch
@echo off
pm2 restart all
pm2 status
pause
```

**logs.bat:**
```batch
@echo off
pm2 logs --lines 50
pause
```

## 🔍 คำสั่งเช็คสถานะระบบ

### ตรวจสอบ Python Environment
```cmd
C:\Users\Administrator\LunarProject\.venv\Scripts\python.exe --version
```

### ตรวจสอบ Port ที่ใช้งาน
```cmd
netstat -an | findstr :5433
netstat -an | findstr :8000
```

### ตรวจสอบ Process ที่รัน
```cmd
tasklist | findstr python
tasklist | findstr pm2
```

## ⚠️ หมายเหตุสำคัญ

1. **Path ต้องถูกต้อง**: ตรวจสอบให้แน่ใจว่า path ใน config file ถูกต้อง
2. **Python Virtual Environment**: ต้องใช้ python จาก venv ที่กำหนด
3. **Logs Directory**: ต้องมีโฟลเดอร์ `logs` ก่อนรัน
4. **Permissions**: รันใน Command Prompt ที่มี Administrator rights
5. **Port Conflicts**: ตรวจสอบ port ก่อนรันเสมอ

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
```