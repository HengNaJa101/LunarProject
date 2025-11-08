-- ===================================================================
-- Thai Lunar Calendar Database Setup SQL
-- สำหรับสร้าง database และ table ด้วยตัวเอง
-- ===================================================================

-- 1. สร้าง Database (รันใน default database หรือ pgAdmin)
-- CREATE DATABASE thai_lunar_db OWNER postgres;

-- 2. เชื่อมต่อ database thai_lunar_db แล้วรัน SQL ด้านล่าง

-- ===================================================================
-- สร้าง Table lunar_calendar
-- ===================================================================

DROP TABLE IF EXISTS lunar_calendar CASCADE;

CREATE TABLE lunar_calendar (
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================================
-- สร้าง Indexes เพื่อ Performance
-- ===================================================================

CREATE INDEX idx_solar_date ON lunar_calendar(solar_date);
CREATE INDEX idx_lunar_date ON lunar_calendar(lunar_year, lunar_month, lunar_day);
CREATE INDEX idx_created_at ON lunar_calendar(created_at);

-- ===================================================================
-- ใส่ข้อมูลตัวอย่าง (ตัวอย่าง 10 รายการ)
-- ===================================================================

INSERT INTO lunar_calendar 
(solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month)
VALUES 
('2024-01-01', 2567, 1, 1, 'มกราคม', 'วันจันทร์', 'มะเมีย', 'กบ', FALSE),
('2024-01-02', 2567, 1, 2, 'มกราคม', 'วันอังคาร', 'มะเมีย', 'ขาล', FALSE),
('2024-01-03', 2567, 1, 3, 'มกราคม', 'วันพุธ', 'มะเมีย', 'เถาะ', FALSE),
('2024-01-04', 2567, 1, 4, 'มกราคม', 'วันพฤหัสบดี', 'มะเมีย', 'มะโรง', FALSE),
('2024-01-05', 2567, 1, 5, 'มกราคม', 'วันศุกร์', 'มะเมีย', 'มะเส็ง', FALSE),
('2024-02-01', 2567, 2, 1, 'กุมภาพันธ์', 'วันพฤหัสบดี', 'มะเมีย', 'ระกา', FALSE),
('2024-03-01', 2567, 3, 1, 'มีนาคม', 'วันศุกร์', 'มะเมีย', 'จอ', FALSE),
('2024-04-01', 2567, 4, 1, 'เมษายน', 'วันจันทร์', 'มะเมีย', 'กุน', FALSE),
('2024-05-01', 2567, 5, 1, 'พฤษภาคม', 'วันพุธ', 'มะเมีย', 'ระเด่น', FALSE),
('2024-06-01', 2567, 6, 1, 'มิถุนายน', 'วันเสาร์', 'มะเมีย', 'ผิง', FALSE);

-- ===================================================================
-- ตรวจสอบข้อมูลที่ใส่
-- ===================================================================

SELECT COUNT(*) as total_records FROM lunar_calendar;

SELECT 
    solar_date,
    lunar_year,
    lunar_month,
    lunar_day,
    lunar_month_name,
    day_name
FROM lunar_calendar 
ORDER BY solar_date 
LIMIT 10;

-- ===================================================================
-- สร้าง Function สำหรับ Update timestamp (Optional)
-- ===================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_lunar_calendar_updated_at 
    BEFORE UPDATE ON lunar_calendar 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ===================================================================
-- ตัวอย่าง Queries ที่เป็นประโยชน์
-- ===================================================================

-- หาข้อมูลปฏิทินจันทรคติของวันนี้
SELECT * FROM lunar_calendar WHERE solar_date = CURRENT_DATE;

-- หาข้อมูลของเดือนปัจจุบัน
SELECT * FROM lunar_calendar 
WHERE EXTRACT(YEAR FROM solar_date) = EXTRACT(YEAR FROM CURRENT_DATE)
  AND EXTRACT(MONTH FROM solar_date) = EXTRACT(MONTH FROM CURRENT_DATE)
ORDER BY solar_date;

-- สถิติข้อมูลตามปี
SELECT 
    EXTRACT(YEAR FROM solar_date) as year,
    COUNT(*) as record_count
FROM lunar_calendar 
GROUP BY EXTRACT(YEAR FROM solar_date)
ORDER BY year;

-- หาวันที่มีราศีเดียวกัน
SELECT zodiac_year, COUNT(*) as count
FROM lunar_calendar 
GROUP BY zodiac_year 
ORDER BY count DESC;

-- ===================================================================
-- ข้อมูลการใช้งาน
-- ===================================================================

/*
การใช้งาน:

1. ใน pgAdmin:
   - คลิกขวาที่ "Databases" → Create → Database
   - ชื่อ: thai_lunar_db
   - กด Save
   - คลิกที่ database ใหม่ → Tools → Query Tool
   - Copy & Paste SQL นี้และรัน

2. ใน Command Line:
   psql -U postgres -d thai_lunar_db -f thai_lunar_setup.sql

3. ตรวจสอบผลลัพธ์:
   SELECT COUNT(*) FROM lunar_calendar;
*/