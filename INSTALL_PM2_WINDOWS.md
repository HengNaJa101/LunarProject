# คำแนะนำการติดตั้ง PM2 บน Windows Server 2016

## ขั้นตอนที่ 1: ติดตั้ง Node.js

1. ดาวน์โหลด Node.js LTS จาก: https://nodejs.org/
   - เลือก "Windows Installer (.msi)" สำหรับ x64
   - เวอร์ชันแนะนำ: Node.js 18.x LTS หรือ 20.x LTS

2. รันไฟล์ .msi และติดตั้งตามขั้นตอน
   - ติ๊กถูก "Add to PATH" (ควรติ๊กอยู่แล้วโดยอัตโนมัติ)

3. ทดสอบการติดตั้ง:
```cmd
node --version
npm --version
```

## ขั้นตอนที่ 2: ติดตั้ง PM2

```cmd
npm install -g pm2
```

## ขั้นตอนที่ 3: ติดตั้ง PM2 Windows Service (สำคัญมาก!)

```cmd
npm install -g pm2-windows-service
pm2-service-install
```

## ขั้นตอนที่ 4: ตั้งค่า PM2 ให้เริ่มอัตโนมัติ

```cmd
pm2 startup
```

## ขั้นตอนที่ 5: ติดตั้ง Python Dependencies

```cmd
# ไปที่โฟลเดอร์โปรเจ็ค
cd C:\path\to\your\LunarProject

# สร้าง virtual environment
python -m venv venv

# เปิดใช้งาน virtual environment
venv\Scripts\activate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

## ขั้นตอนที่ 6: แก้ไขไฟล์ ecosystem.config.js

แก้ไขพาธให้ถูกต้องสำหรับ Windows:

```javascript
module.exports = {
  apps: [{
    name: 'lunar-project',
    script: 'FinishLunar.py',
    interpreter: 'C:/path/to/your/LunarProject/venv/Scripts/python.exe',
    cwd: 'C:/path/to/your/LunarProject',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
```

## ขั้นตอนที่ 7: เริ่มใช้งาน

```cmd
# สร้างโฟลเดอร์ logs
mkdir logs

# เริ่ม PM2
pm2 start ecosystem.config.js

# บันทึกการตั้งค่า
pm2 save

# ตรวจสอบสถานะ
pm2 status
pm2 logs
```

## คำสั่งที่มีประโยชน์:

```cmd
pm2 list                    # ดูรายการ processes
pm2 restart lunar-project   # รีสตาร์ท
pm2 stop lunar-project      # หยุด
pm2 delete lunar-project    # ลบ process
pm2 logs lunar-project      # ดู logs
pm2 monit                   # monitor real-time
```

## หมายเหตุสำคัญ:
1. ต้องใช้ Command Prompt หรือ PowerShell ในโหมด Administrator
2. ตรวจสอบให้แน่ใจว่า Python อยู่ใน PATH
3. PM2 Windows Service จำเป็นสำหรับการเริ่มอัตโนมัติเมื่อ restart server
4. ใช้พาธแบบเต็ม (absolute path) ใน ecosystem.config.js