-- Thai Lunar Calendar Database Setup
-- สร้างฐานข้อมูลและตารางสำหรับปฏิทินจันทรคติไทย

-- สร้างฐานข้อมูล (รันใน pgAdmin เป็น superuser)
-- CREATE DATABASE thai_lunar_db;

-- เชื่อมต่อกับฐานข้อมูล thai_lunar_db แล้วรันคำสั่งต่อไปนี้:

-- สร้างตาราง lunar_calendar
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
CREATE INDEX IF NOT EXISTS idx_lunar_year_month ON lunar_calendar(lunar_year, lunar_month);

-- ลบข้อมูลเก่า (ถ้ามี)
TRUNCATE TABLE lunar_calendar;

-- ใส่ข้อมูลตัวอย่างสำหรับทดสอบ
INSERT INTO lunar_calendar 
(solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month)
VALUES 
-- ข้อมูลปี 2024-2025
('2024-11-01', 2567, 10, 1, 'เดือน 10', 'วันศุกร์', 'มะเมีย', 'มอ', FALSE),
('2024-11-08', 2567, 10, 8, 'เดือน 10', 'วันศุกร์', 'มะเมีย', 'กุน', FALSE),
('2024-11-15', 2567, 10, 15, 'เดือน 10', 'วันศุกร์', 'มะเมีย', 'กา', FALSE),
('2024-12-01', 2567, 11, 1, 'เดือน 11', 'วันอาทิตย์', 'มะเมีย', 'กิน', FALSE),
('2024-12-15', 2567, 11, 15, 'เดือน 11', 'วันอาทิตย์', 'มะเมีย', 'กง', FALSE),

('2025-01-01', 2568, 12, 2, 'เดือน 12', 'วันพุธ', 'มะโรง', 'กบ', FALSE),
('2025-01-15', 2568, 12, 16, 'เดือน 12', 'วันพุธ', 'มะโรง', 'ขาล', FALSE),
('2025-01-29', 2568, 1, 1, 'เดือน 1', 'วันพุธ', 'มะโรง', 'มะเมีย', FALSE),
('2025-02-01', 2568, 1, 4, 'เดือน 1', 'วันเสาร์', 'มะโรง', 'ระกา', FALSE),
('2025-02-15', 2568, 1, 18, 'เดือน 1', 'วันเสาร์', 'มะโรง', 'จอ', FALSE),
('2025-03-01', 2568, 2, 2, 'เดือน 2', 'วันเสาร์', 'มะโรง', 'กย', FALSE),
('2025-03-15', 2568, 2, 16, 'เดือน 2', 'วันเสาร์', 'มะโรง', 'วอก', FALSE),
('2025-04-01', 2568, 3, 4, 'เดือน 3', 'วันอังคาร', 'มะโรง', 'ขุน', FALSE),
('2025-05-01', 2568, 4, 5, 'เดือน 4', 'วันพฤหัสบดี', 'มะโรง', 'กิน', FALSE),
('2025-06-01', 2568, 5, 7, 'เดือน 5', 'วันอาทิตย์', 'มะโรง', 'กา', FALSE),
('2025-07-01', 2568, 6, 8, 'เดือน 6', 'วันอังคาร', 'มะโรง', 'งูใหญ่', FALSE),
('2025-08-01', 2568, 7, 10, 'เดือน 7', 'วันศุกร์', 'มะโรง', 'เถาะ', FALSE),
('2025-09-01', 2568, 8, 12, 'เดือน 8', 'วันจันทร์', 'มะโรง', 'ค่า', FALSE),
('2025-10-01', 2568, 9, 13, 'เดือน 9', 'วันพุธ', 'มะโรง', 'จาน', FALSE),
('2025-11-01', 2568, 10, 15, 'เดือน 10', 'วันเสาร์', 'มะโรง', 'มอ', FALSE),
('2025-11-08', 2568, 10, 22, 'เดือน 10', 'วันเสาร์', 'มะโรง', 'กุน', FALSE),
('2025-11-09', 2568, 10, 23, 'เดือน 10', 'วันอาทิตย์', 'มะโรง', 'กา', FALSE),
('2025-12-01', 2568, 11, 16, 'เดือน 11', 'วันจันทร์', 'มะโรง', 'กิน', FALSE);

-- ตรวจสอบผลลัพธ์
SELECT COUNT(*) as total_records FROM lunar_calendar;
SELECT 'Sample data inserted successfully' as status;
SELECT * FROM lunar_calendar ORDER BY solar_date LIMIT 10;