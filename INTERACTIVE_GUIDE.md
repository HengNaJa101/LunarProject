# 🌙 Thai Lunar Calendar - Interactive Mode

## วิธีรัน Interactive Mode ด้วย PM2

### 1. 🚀 รัน Interactive Mode เท่านั้น
```bash
# รัน interactive mode อย่างเดียว
pm2 start interactive_lunar.py --name "lunar-interactive" --interpreter .venv\Scripts\python.exe -- --pm2 --interactive

# ดู logs แบบ real-time
pm2 logs lunar-interactive
```

### 2. 🔧 รันทุก Services พร้อมกัน
```bash
# รันทั้ง background service, interactive mode, และ web api
pm2 start ecosystem-interactive.config.js

# ดูสถานะทั้งหมด
pm2 status
```

### 3. 📋 จัดการ Interactive Session
```bash
# ดู logs ของ interactive mode
pm2 logs lunar-interactive --lines 50

# หยุด interactive mode
pm2 stop lunar-interactive

# รีสตาร์ท interactive mode
pm2 restart lunar-interactive

# ลบ interactive mode
pm2 delete lunar-interactive
```

## การใช้งาน Interactive Mode

### Input ตัวอย่าง:
1. **วันที่เกิด**: 15 (1-31)
2. **เดือนเกิด**: 5 (1-12) 
3. **ปีเกิด**: 2520 (พ.ศ.)
4. **อายุครรภ์**: 9 (7,8,9,0)
5. **ช่วงเวลา**: 1 (1=กลางวัน, 2=กลางคืน)

### Default Values:
- ถ้าไม่ใส่ค่า จะใช้ค่า default ที่แสดงใน `[default: ...]`
- กด Enter เพื่อใช้ค่า default

### การทำงาน:
1. โปรแกรมจะคำนวณจันทรคติไทย
2. แสดงผลลัพธ์แบบละเอียด
3. ถามว่าต้องการคำนวณต่อหรือหยุด
4. เลือก 1 = คำนวณใหม่, 2 = หยุดโปรแกรม

## ตัวอย่างการใช้งาน

### รันแบบ Interactive เฉพาะ:
```bash
cd C:\Users\Administrator\LunarProject
.venv\Scripts\activate
pm2 start interactive_lunar.py --name "lunar-calc" --interpreter .venv\Scripts\python.exe -- --pm2 --interactive
pm2 logs lunar-calc
```

### รันครบทุก Service:
```bash
cd C:\Users\Administrator\LunarProject
git pull origin main
.venv\Scripts\activate
pip install flask
pm2 start ecosystem-interactive.config.js
pm2 status
```

## Services ที่จะรัน:

1. **lunar-service**: Background service (ตัวเดิม)
2. **lunar-interactive**: Interactive mode สำหรับใส่วันเดือนปี
3. **lunar-web-api**: Web API สำหรับเรียกใช้ผ่าน HTTP

## Logs Location:
- Interactive: `./logs/interactive-out.log`
- Service: `./logs/service-out.log` 
- Web API: `./logs/web-out.log`

## การออกจากโปรแกรม:
- ใน Interactive mode: เลือก 2 หรือกด Ctrl+C
- PM2 จะจัดการ process ให้อัตโนมัติ