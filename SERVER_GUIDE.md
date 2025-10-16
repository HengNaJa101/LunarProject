# 🌙 Thai Lunar Calendar Server - Port 5433

## การรันโปรแกรมผ่าน Command Line

### วิธีที่ 1: รันด้วย Batch File (แนะนำ)
```cmd
# ไปยัง directory โปรเจค
cd C:\Users\Administrator\LunarProject

# รัน server
start_server.bat
```

### วิธีที่ 2: รันด้วย Python โดยตรง
```cmd
# ไปยัง directory โปรเจค
cd C:\Users\Administrator\LunarProject

# เปิดใช้ virtual environment
.venv\Scripts\activate

# รัน server
python lunar_server.py
```

### วิธีที่ 3: รันด้วย PM2
```cmd
# รัน server ด้วย PM2
pm2 start lunar_server.py --name "lunar-server-5433" --interpreter .venv\Scripts\python.exe

# ดูสถานะ
pm2 status

# ดู logs
pm2 logs lunar-server-5433
```

## การใช้งาน Server

### การเชื่อมต่อด้วย Telnet
```cmd
telnet localhost 5433
```

### การเชื่อมต่อด้วย PowerShell
```powershell
$client = New-Object System.Net.Sockets.TcpClient("localhost", 5433)
$stream = $client.GetStream()
$writer = New-Object System.IO.StreamWriter($stream)
$reader = New-Object System.IO.StreamReader($stream)

# อ่านข้อความต้อนรับ
$reader.ReadLine()

# ส่งข้อมูล JSON
$data = @{
    birth_year = 2520
    birth_month = 5
    birth_day = 15
    pregnancy_months = 9
    time_period = "กลางวัน"
} | ConvertTo-Json -Compress

$writer.WriteLine($data)
$writer.Flush()

# อ่านผลลัพธ์
$result = $reader.ReadLine()
Write-Host $result

# ปิดการเชื่อมต่อ
$writer.WriteLine("exit")
$client.Close()
```

### การเชื่อมต่อด้วย Python Client
```python
import socket
import json

# เชื่อมต่อ server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5433))

# รับข้อความต้อนรับ
welcome = client.recv(4096).decode('utf-8')
print("Server:", welcome)

# ส่งข้อมูลคำนวณ
data = {
    "birth_year": 2520,
    "birth_month": 5,
    "birth_day": 15,
    "pregnancy_months": 9,
    "time_period": "กลางวัน"
}

client.send(json.dumps(data).encode('utf-8'))

# รับผลลัพธ์
result = client.recv(8192).decode('utf-8')
response = json.loads(result)
print("ผลลัพธ์:", response)

# ปิดการเชื่อมต่อ
client.send(b"exit")
client.close()
```

## รูปแบบข้อมูล JSON

### ข้อมูลที่ส่งไป (Request)
```json
{
    "birth_year": 2520,
    "birth_month": 5,
    "birth_day": 15,
    "pregnancy_months": 9,
    "time_period": "กลางวัน"
}
```

### ข้อมูลที่ได้รับ (Response)
```json
{
    "status": "success",
    "input": {
        "birth_date": "15/5/2520",
        "pregnancy_months": 9,
        "time_period": "กลางวัน"
    },
    "result": "ข้อมูลจันทรคติแบบละเอียด...",
    "timestamp": "2025-10-16 20:30:45"
}
```

## การหยุด Server

- กด `Ctrl+C` ใน Command Prompt
- ส่งคำสั่ง `exit`, `quit`, หรือ `bye` ผ่าน client
- ใช้ `pm2 stop lunar-server-5433` ถ้ารันด้วย PM2

## การ Debug

### ตรวจสอบ Port
```cmd
netstat -an | findstr 5433
```

### ดู Logs
```cmd
# ถ้ารันด้วย PM2
pm2 logs lunar-server-5433

# ถ้ารันปกติจะแสดงใน console
```

## ตัวอย่างการใช้งานจริง

```cmd
C:\Users\Administrator\LunarProject> start_server.bat
========================================
  Thai Lunar Calendar Server Launcher
========================================

[1/4] กำลังไปยัง directory โปรเจค...
[2/4] กำลังเปิดใช้ virtual environment...
[3/4] ตรวจสอบ dependencies...
✓ Dependencies พร้อมใช้งาน
[4/4] เริ่มต้น Thai Lunar Calendar Server...

🌙 Thai Lunar Calendar Server เริ่มทำงานแล้ว
📡 Host: localhost
🔌 Port: 5433
🌐 URL: http://localhost:5433
⏰ เวลา: 2025-10-16 20:30:15
------------------------------------------------------------
📝 วิธีการใช้งาน:
   - เชื่อมต่อผ่าน telnet หรือ netcat
   - ส่งข้อมูล JSON format
   - กด Ctrl+C เพื่อหยุด server
------------------------------------------------------------
✅ เชื่อมต่อฐานข้อมูลสำเร็จ

🎯 รอการเชื่อมต่อจากลูกค้า...
```