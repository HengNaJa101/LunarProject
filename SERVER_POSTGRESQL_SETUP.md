# 🏗️ PostgreSQL Setup Guide for Windows Server

## 🚨 ปัญหาที่พบ
```
❌ ไม่สามารถเชื่อมต่อ PostgreSQL ได้
```

## 🔧 วิธีแก้ไข (เลือก 1 วิธี)

### วิธีที่ 1: ติดตั้ง PostgreSQL บน Server

#### ขั้นตอนที่ 1: ตรวจสอบสถานะปัจจุบัน
```cmd
cd C:\LunarProjectNew
check_postgresql_server.bat
```

#### ขั้นตอนที่ 2: ติดตั้ง PostgreSQL (ถ้ายังไม่มี)
```cmd
# รันด้วยสิทธิ์ Administrator
install_postgresql_server.bat
```

#### ขั้นตอนที่ 3: ตั้งรหัสผ่าน PostgreSQL
```cmd
# วิธีที่ 1: ใช้ psql
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -c "ALTER USER postgres PASSWORD 'postgres';"

# วิธีที่ 2: ใช้ pgAdmin (GUI)
# เปิด pgAdmin และตั้งรหัสผ่านผ่าน interface
```

#### ขั้นตอนที่ 4: ทดสอบการเชื่อมต่อ
```cmd
cd C:\LunarProjectNew
python smart_database_setup.py
```

### วิธีที่ 2: ใช้ SQLite แทน (ง่ายกว่า)

#### สร้างไฟล์ `database_config_sqlite.py`
```python
import sqlite3
import os

# การตั้งค่าสำหรับ SQLite
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'thai_lunar.db')

def get_sqlite_connection():
    """สร้างการเชื่อมต่อ SQLite"""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    return conn

def setup_sqlite_database():
    """สร้าง database และ table สำหรับ SQLite"""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    
    # สร้าง table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lunar_calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solar_date DATE NOT NULL,
            lunar_year INTEGER NOT NULL,
            lunar_month INTEGER NOT NULL,
            lunar_day INTEGER NOT NULL,
            lunar_month_name TEXT,
            day_name TEXT,
            zodiac_year TEXT,
            zodiac_day TEXT,
            is_leap_month BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ SQLite database setup เสร็จสิ้น")

if __name__ == "__main__":
    setup_sqlite_database()
```

### วิธีที่ 3: ใช้ Docker PostgreSQL

#### ติดตั้ง Docker Desktop
```cmd
winget install Docker.DockerDesktop
```

#### รัน PostgreSQL Container
```cmd
docker run --name postgres-lunar -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:17
```

## 🎯 คำแนะนำ

### สำหรับ Production Server:
- **วิธีที่ 1** (PostgreSQL): เหมาะสำหรับ production, performance ดี
- **วิธีที่ 2** (SQLite): เหมาะสำหรับ development/testing, ง่าย
- **วิธีที่ 3** (Docker): เหมาะสำหรับ container-based deployment

### สำหรับ Testing ด่วน:
ใช้ **SQLite** เพราะ:
- ✅ ไม่ต้องติดตั้งอะไรเพิ่ม
- ✅ ไฟล์ database เดียว
- ✅ รองรับ SQL เหมือน PostgreSQL

## 🚀 Quick Start (SQLite)

```cmd
cd C:\LunarProjectNew
git pull origin main
python database_config_sqlite.py
pm2 start ecosystem-full.config.js
```