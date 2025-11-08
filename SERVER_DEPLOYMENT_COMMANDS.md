# คำสั่งสำหรับรันใน Server
# Thai Lunar Calendar API Deployment Guide

## ขั้นตอนที่ 1: Setup PostgreSQL บน Server
# รันคำสั่งเหล่านี้ใน pgAdmin Query Tool ของ server

# สร้างฐานข้อมูล (ถ้ายังไม่มี)
CREATE DATABASE thai_lunar_db;

# เชื่อมต่อกับฐานข้อมูล thai_lunar_db แล้วรันคำสั่งต่อไปนี้:

# สร้าง table lunar_calendar
CREATE TABLE IF NOT EXISTS lunar_calendar (
    id SERIAL PRIMARY KEY,
    solar_date DATE NOT NULL UNIQUE,
    lunar_year INTEGER NOT NULL,
    lunar_month INTEGER NOT NULL,
    lunar_day INTEGER NOT NULL,
    lunar_month_name VARCHAR(50),
    day_name VARCHAR(50),
    zodiac_year VARCHAR(50),
    zodiac_day VARCHAR(50),
    is_leap_month BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

# สร้าง indexes
CREATE INDEX IF NOT EXISTS idx_solar_date ON lunar_calendar(solar_date);
CREATE INDEX IF NOT EXISTS idx_lunar_date ON lunar_calendar(lunar_year, lunar_month, lunar_day);

# ใส่ข้อมูลตัวอย่าง
INSERT INTO lunar_calendar 
(solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month)
VALUES 
('2024-01-01', 2567, 1, 1, 'มกราคม', 'วันจันทร์', 'มะเมีย', 'กบ', FALSE),
('2024-01-02', 2567, 1, 2, 'มกราคม', 'วันอังคาร', 'มะเมีย', 'ขาล', FALSE),
('2024-01-03', 2567, 1, 3, 'มกราคม', 'วันพุธ', 'มะเมีย', 'เถาะ', FALSE),
('2024-02-01', 2567, 2, 1, 'กุมภาพันธ์', 'วันพฤหัสบดี', 'มะเมีย', 'ระกา', FALSE),
('2024-03-01', 2567, 3, 1, 'มีนาคม', 'วันศุกร์', 'มะเมีย', 'จอ', FALSE),
('2024-11-08', 2567, 12, 8, 'พฤศจิกายน', 'วันศุกร์', 'มะเมีย', 'กุน', FALSE),
('2025-11-08', 2568, 12, 8, 'พฤศจิกายน', 'วันศุกร์', 'มะโรง', 'กุน', FALSE)
ON CONFLICT (solar_date) DO NOTHING;

# ตรวจสอบผลลัพธ์
SELECT COUNT(*) as total_records FROM lunar_calendar;
SELECT * FROM lunar_calendar ORDER BY solar_date;

## ขั้นตอนที่ 2: รันคำสั่งใน Terminal Server

# 1. ไปยัง directory โปรเจค
cd /path/to/LunarProject

# 2. ดึงโค้ดล่าสุดจาก GitHub
git pull origin main

# 3. ติดตั้ง Python packages ที่จำเป็น
pip install Flask psycopg2-binary

# 4. ทดสอบการเชื่อมต่อฐานข้อมูล
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='thai_lunar_db',
        user='postgres',
        password='123456'
    )
    print('✅ PostgreSQL connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ PostgreSQL connection failed: {e}')
"

# 5. ทดสอบรัน API แบบ manual (ทดสอบ)
python thai_lunar_api.py

# 6. หยุด manual test (Ctrl+C) แล้วใช้ PM2 deploy
pm2 start ecosystem-api.config.js

# 7. ตรวจสอบสถานะ PM2
pm2 status
pm2 logs thai-lunar-api

# 8. ทดสอบ API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/lunar/today
curl http://localhost:8000/usersinfo/get/profile

## ขั้นตอนที่ 3: ตรวจสอบและ Debug (ถ้าจำเป็น)

# ตรวจสอบ logs หาก API ไม่ทำงาน
pm2 logs thai-lunar-api --lines 50

# หยุดและรีสตาร์ท API
pm2 restart thai-lunar-api

# หยุด API
pm2 stop thai-lunar-api

# ลบ API จาก PM2
pm2 delete thai-lunar-api

## ขั้นตอนที่ 4: การ Monitor และ Maintain

# ดู status ทั้งหมด
pm2 status

# ดู resource usage
pm2 monit

# Save configuration PM2
pm2 save

# Setup PM2 startup
pm2 startup
# (ทำตามคำสั่งที่แสดงออกมา)

## URLs สำหรับทดสอบ:
# Health Check: http://your-server-ip:8000/health
# User Profile: http://your-server-ip:8000/usersinfo/get/profile  
# Today Data: http://your-server-ip:8000/lunar/today
# Specific Date: http://your-server-ip:8000/lunar/date/2024-11-08
# Statistics: http://your-server-ip:8000/lunar/stats