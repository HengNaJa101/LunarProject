# 🌙 Thai Lunar Calendar Project - การใช้งาน

## ตัวเลือกการใช้งาน

### 1. 🖥️ Command Line Interface
```bash
cd C:\Users\Administrator\LunarProject
.venv\Scripts\activate
python FinishLunar.py
```

### 2. 🔧 Background Service (ปัจจุบัน)
```bash
pm2 status
pm2 logs lunar-project
pm2 restart lunar-project
```

### 3. 📡 Web API Service
```bash
# ติดตั้ง Flask
pip install flask

# รัน Web API
pm2 start ecosystem-full.config.js

# หรือรันด้วยตัวเอง
python web_api.py
```

API จะรันที่: http://localhost:5000

#### API Endpoints:
- `POST /lunar` - คำนวณจันทรคติ
- `GET /health` - ตรวจสอบสถานะ

### 4. 🌐 Web Interface
เปิดไฟล์ `templates/index.html` ในเบราว์เซอร์

## ตัวอย่างการใช้งาน API

### cURL
```bash
curl -X POST http://localhost:5000/lunar \
  -H "Content-Type: application/json" \
  -d '{
    "birth_year": 2520,
    "birth_month": 5,
    "birth_day": 15,
    "pregnancy_months": 9,
    "time_period": "กลางวัน"
  }'
```

### PowerShell
```powershell
$body = @{
    birth_year = 2520
    birth_month = 5
    birth_day = 15
    pregnancy_months = 9
    time_period = "กลางวัน"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/lunar" -Method POST -Body $body -ContentType "application/json"
```

### Python
```python
import requests

data = {
    "birth_year": 2520,
    "birth_month": 5,
    "birth_day": 15,
    "pregnancy_months": 9,
    "time_period": "กลางวัน"
}

response = requests.post("http://localhost:5000/lunar", json=data)
result = response.json()
print(result)
```

## PM2 Commands
```bash
pm2 status                    # ดูสถานะทั้งหมด
pm2 logs lunar-project        # ดู logs service
pm2 logs lunar-web-api        # ดู logs web api
pm2 restart all               # รีสตาร์ททั้งหมด
pm2 stop all                  # หยุดทั้งหมด
pm2 delete all                # ลบทั้งหมด
pm2 save                      # บันทึก configuration
pm2 monit                     # monitor real-time
```

## File Structure
```
LunarProject/
├── FinishLunar.py              # โปรแกรมหลัก
├── web_api.py                  # Web API
├── ecosystem.config.js         # PM2 config (service only)
├── ecosystem-full.config.js    # PM2 config (service + web api)
├── templates/
│   └── index.html             # Web interface
├── logs/                      # Log files
└── .venv/                     # Virtual environment
```

## การพัฒนาต่อ
1. เพิ่ม authentication ใน API
2. สร้าง mobile app ที่เรียกใช้ API
3. เพิ่มฟีเจอร์บันทึกข้อมูล
4. สร้าง admin panel
5. เพิ่ม caching สำหรับ performance