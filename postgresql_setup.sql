# คำสั่งสำหรับ Setup PostgreSQL Database บน Server
# รันใน pgAdmin Query Tool หรือ psql command line

-- ขั้นตอนที่ 1: สร้างฐานข้อมูล (ถ้ายังไม่มี)
CREATE DATABASE thai_lunar_db;

-- ขั้นตอนที่ 2: เชื่อมต่อกับฐานข้อมูล thai_lunar_db และรันคำสั่งต่อไปนี้:

-- สร้าง table lunar_calendar (ถ้ายังไม่มี)
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

-- สร้าง indexes เพื่อเพิ่มประสิทธิภาพ
CREATE INDEX IF NOT EXISTS idx_solar_date ON lunar_calendar(solar_date);
CREATE INDEX IF NOT EXISTS idx_lunar_date ON lunar_calendar(lunar_year, lunar_month, lunar_day);

-- ลบข้อมูลเก่า (ถ้ามี)
DELETE FROM lunar_calendar;

-- ใส่ข้อมูลตัวอย่าง สำหรับทดสอบ API
INSERT INTO lunar_calendar 
(solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month)
VALUES 
-- ข้อมูลปี 2024
('2024-01-01', 2567, 1, 1, 'มกราคม', 'วันจันทร์', 'มะเมีย', 'กบ', FALSE),
('2024-01-02', 2567, 1, 2, 'มกราคม', 'วันอังคาร', 'มะเมีย', 'ขาล', FALSE),
('2024-01-03', 2567, 1, 3, 'มกราคม', 'วันพุธ', 'มะเมีย', 'เถาะ', FALSE),
('2024-02-01', 2567, 2, 1, 'กุมภาพันธ์', 'วันพฤหัสบดี', 'มะเมีย', 'ระกา', FALSE),
('2024-03-01', 2567, 3, 1, 'มีนาคม', 'วันศุกร์', 'มะเมีย', 'จอ', FALSE),
('2024-04-01', 2567, 4, 1, 'เมษายน', 'วันจันทร์', 'มะเมีย', 'กย', FALSE),
('2024-05-01', 2567, 5, 1, 'พฤษภาคม', 'วันพุธ', 'มะเมีย', 'ขุน', FALSE),
('2024-06-01', 2567, 6, 1, 'มิถุนายน', 'วันเสาร์', 'มะเมีย', 'กิน', FALSE),
('2024-07-01', 2567, 7, 1, 'กรกฎาคม', 'วันจันทร์', 'มะเมีย', 'กา', FALSE),
('2024-08-01', 2567, 8, 1, 'สิงหาคม', 'วันพฤหัสบดี', 'มะเมีย', 'กง', FALSE),
('2024-09-01', 2567, 9, 1, 'กันยายน', 'วันอาทิตย์', 'มะเมีย', 'จาน', FALSE),
('2024-10-01', 2567, 10, 1, 'ตุลาคม', 'วันอังคาร', 'มะเมีย', 'เถาะ', FALSE),
('2024-11-01', 2567, 11, 1, 'พฤศจิกายน', 'วันศุกร์', 'มะเมีย', 'มอ', FALSE),
('2024-11-08', 2567, 12, 8, 'พฤศจิกายน', 'วันศุกร์', 'มะเมีย', 'กุน', FALSE),
('2024-12-01', 2567, 12, 1, 'ธันวาคม', 'วันอาทิตย์', 'มะเมีย', 'กา', FALSE),

-- ข้อมูลปี 2025
('2025-01-01', 2568, 1, 1, 'มกราคม', 'วันพุธ', 'มะโรง', 'กบ', FALSE),
('2025-01-02', 2568, 1, 2, 'มกราคม', 'วันพฤหัสบดี', 'มะโรง', 'ขาล', FALSE),
('2025-02-01', 2568, 2, 1, 'กุมภาพันธ์', 'วันเสาร์', 'มะโรง', 'ระกา', FALSE),
('2025-03-01', 2568, 3, 1, 'มีนาคม', 'วันเสาร์', 'มะโรง', 'จอ', FALSE),
('2025-04-01', 2568, 4, 1, 'เมษายน', 'วันอังคาร', 'มะโรง', 'กย', FALSE),
('2025-05-01', 2568, 5, 1, 'พฤษภาคม', 'วันพฤหัสบดี', 'มะโรง', 'ขุน', FALSE),
('2025-06-01', 2568, 6, 1, 'มิถุนายน', 'วันอาทิตย์', 'มะโรง', 'กิน', FALSE),
('2025-07-01', 2568, 7, 1, 'กรกฎาคม', 'วันอังคาร', 'มะโรง', 'กา', FALSE),
('2025-08-01', 2568, 8, 1, 'สิงหาคม', 'วันศุกร์', 'มะโรง', 'กง', FALSE),
('2025-09-01', 2568, 9, 1, 'กันยายน', 'วันจันทร์', 'มะโรง', 'จาน', FALSE),
('2025-10-01', 2568, 10, 1, 'ตุลาคม', 'วันพุธ', 'มะโรง', 'เถาะ', FALSE),
('2025-11-01', 2568, 11, 1, 'พฤศจิกายน', 'วันเสาร์', 'มะโรง', 'มอ', FALSE),
('2025-11-08', 2568, 12, 8, 'พฤศจิกายน', 'วันศุกร์', 'มะโรง', 'กุน', FALSE),
('2025-12-01', 2568, 12, 1, 'ธันวาคม', 'วันจันทร์', 'มะโรง', 'กา', FALSE);

-- ตรวจสอบผลลัพธ์
SELECT COUNT(*) as total_records FROM lunar_calendar;
SELECT 'ข้อมูลตัวอย่าง:' as status;
SELECT solar_date, lunar_year, lunar_month, lunar_day, day_name, zodiac_year, zodiac_day 
FROM lunar_calendar 
ORDER BY solar_date 
LIMIT 10;

-- ตรวจสอบข้อมูลวันนี้
SELECT 'ข้อมูลวันที่ปัจจุบัน:' as status;
SELECT * FROM lunar_calendar WHERE solar_date = CURRENT_DATE;

-- หากไม่มีข้อมูลวันที่ปัจจุบัน แสดงข้อมูลล่าสุด
SELECT 'ข้อมูลล่าสุดในระบบ:' as status;
SELECT * FROM lunar_calendar ORDER BY solar_date DESC LIMIT 5;