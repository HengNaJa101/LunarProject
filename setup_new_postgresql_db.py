# -*- coding: utf-8 -*-
"""
Database Setup for New PostgreSQL Database
สร้าง table และเตรียมข้อมูลสำหรับ database ใหม่
"""

import psycopg2
import sqlite3
import os
from datetime import datetime, date

# การตั้งค่า PostgreSQL ใหม่
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thai_lunar_db',  # database ใหม่ที่สร้าง
    'user': 'postgres',
    'password': 'postgres'  # เปลี่ยนเป็นรหัสผ่านจริง
}

# การตั้งค่า SQLite เก่า (ถ้ามี)
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'thai_lunar.db')

def test_postgresql_connection():
    """ทดสอบการเชื่อมต่อ PostgreSQL database ใหม่"""
    try:
        print("🔍 ทดสอบการเชื่อมต่อ PostgreSQL...")
        
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL Version: {version}")
        print(f"✅ Database: {POSTGRES_CONFIG['database']}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("💡 แนะนำ:")
        print("   1. ตรวจสอบว่าสร้าง database 'thai_lunar_db' แล้วหรือยัง")
        print("   2. ตรวจสอบรหัสผ่าน postgres")
        print("   3. แก้ไข POSTGRES_CONFIG ในไฟล์นี้")
        return False

def create_lunar_calendar_table():
    """สร้าง table lunar_calendar"""
    try:
        print("📊 สร้าง table lunar_calendar...")
        
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        
        # ลบ table เก่าถ้ามี (ระวัง!)
        cursor.execute("DROP TABLE IF EXISTS lunar_calendar CASCADE")
        
        # สร้าง table ใหม่
        create_table_sql = """
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
        """
        
        cursor.execute(create_table_sql)
        
        # สร้าง indexes สำหรับ performance
        indexes = [
            "CREATE INDEX idx_solar_date ON lunar_calendar(solar_date);",
            "CREATE INDEX idx_lunar_date ON lunar_calendar(lunar_year, lunar_month, lunar_day);",
            "CREATE INDEX idx_created_at ON lunar_calendar(created_at);"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        conn.commit()
        print("✅ สร้าง table และ indexes สำเร็จ")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False

def generate_sample_lunar_data():
    """สร้างข้อมูลตัวอย่างปฏิทินจันทรคติ"""
    
    sample_data = []
    
    # สร้างข้อมูล 365 วันสำหรับปี 2024
    from datetime import timedelta
    
    start_date = date(2024, 1, 1)
    
    month_names = [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    
    day_names = ["วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์", "วันอาทิตย์"]
    
    zodiac_years = ["มะเมีย", "วอก", "ระกา", "จอ", "กุน", "ระเด่น", "มะเส็ง", "วิงมะตัน", "ขาล", "เถาะ", "ขาบ", "กาจ"]
    zodiac_days = ["กบ", "ขาล", "เถาะ", "มะโรง", "มะเส็ง", "มะใส", "วอก", "ระกา", "จอ", "กุน", "ระเด่น", "ผิง"]
    
    for day_offset in range(365):
        current_date = start_date + timedelta(days=day_offset)
        
        # คำนวณปฏิทินจันทรคติแบบง่าย (สำหรับตัวอย่าง)
        lunar_year = current_date.year + 543  # พ.ศ.
        lunar_month = ((current_date.month - 1 + day_offset // 30) % 12) + 1
        lunar_day = (day_offset % 30) + 1
        
        lunar_month_name = month_names[lunar_month - 1] if lunar_month <= 12 else f"เดือน{lunar_month}"
        day_name = day_names[current_date.weekday()]
        zodiac_year = zodiac_years[lunar_year % 12]
        zodiac_day = zodiac_days[day_offset % 12]
        
        sample_data.append((
            current_date,
            lunar_year,
            lunar_month,
            lunar_day,
            lunar_month_name,
            day_name,
            zodiac_year,
            zodiac_day,
            False  # is_leap_month
        ))
    
    return sample_data

def insert_sample_data():
    """ใส่ข้อมูลตัวอย่างลง PostgreSQL"""
    try:
        print("📝 สร้างและใส่ข้อมูลตัวอย่าง...")
        
        # สร้างข้อมูลตัวอย่าง
        sample_data = generate_sample_lunar_data()
        print(f"📊 สร้างข้อมูล {len(sample_data)} รายการ")
        
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        
        # ใส่ข้อมูล
        insert_sql = """
            INSERT INTO lunar_calendar 
            (solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name,
             day_name, zodiac_year, zodiac_day, is_leap_month)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (solar_date) DO NOTHING
        """
        
        cursor.executemany(insert_sql, sample_data)
        conn.commit()
        
        # ตรวจสอบข้อมูลที่ใส่
        cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        count = cursor.fetchone()[0]
        print(f"✅ ใส่ข้อมูล {count} รายการสำเร็จ")
        
        # แสดงข้อมูลตัวอย่าง
        cursor.execute("""
            SELECT solar_date, lunar_year, lunar_month, lunar_day, day_name 
            FROM lunar_calendar 
            ORDER BY solar_date 
            LIMIT 5
        """)
        samples = cursor.fetchall()
        
        print("📋 ตัวอย่างข้อมูลที่ใส่:")
        for row in samples:
            print(f"   {row[0]} → {row[1]}/{row[2]}/{row[3]} ({row[4]})")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return False

def migrate_from_sqlite():
    """ย้ายข้อมูลจาก SQLite (ถ้ามี)"""
    try:
        if not os.path.exists(SQLITE_DB_PATH):
            print("⚠️ ไม่พบ SQLite database - ข้าม migration")
            return True
        
        print("🔄 ย้ายข้อมูลจาก SQLite...")
        
        # อ่านจาก SQLite
        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        sqlite_cursor.execute("SELECT * FROM lunar_calendar")
        rows = sqlite_cursor.fetchall()
        
        if len(rows) == 0:
            print("⚠️ ไม่มีข้อมูลใน SQLite")
            return True
        
        print(f"📊 พบข้อมูล {len(rows)} รายการใน SQLite")
        
        # ใส่ลง PostgreSQL
        pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
        pg_cursor = pg_conn.cursor()
        
        migrated_count = 0
        
        for row in rows:
            try:
                pg_cursor.execute("""
                    INSERT INTO lunar_calendar 
                    (solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name,
                     day_name, zodiac_year, zodiac_day, is_leap_month)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (solar_date) DO NOTHING
                """, (
                    row['solar_date'],
                    row['lunar_year'],
                    row['lunar_month'],
                    row['lunar_day'],
                    row['lunar_month_name'],
                    row['day_name'],
                    row['zodiac_year'],
                    row['zodiac_day'],
                    row['is_leap_month']
                ))
                migrated_count += 1
                
            except Exception as e:
                print(f"⚠️ Error migrating row: {e}")
                continue
        
        pg_conn.commit()
        print(f"✅ ย้ายข้อมูล {migrated_count} รายการสำเร็จ")
        
        # ปิดการเชื่อมต่อ
        sqlite_cursor.close()
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error migrating from SQLite: {e}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 PostgreSQL Database Setup for Thai Lunar Calendar")
    print("=" * 70)
    
    # 1. ทดสอบการเชื่อมต่อ
    if not test_postgresql_connection():
        return False
    
    # 2. สร้าง table
    if not create_lunar_calendar_table():
        return False
    
    # 3. ย้ายข้อมูลจาก SQLite (ถ้ามี)
    migrate_from_sqlite()
    
    # 4. ใส่ข้อมูลตัวอย่าง (ถ้ายังไม่มี)
    if not insert_sample_data():
        return False
    
    print("\n🎯 Database setup เสร็จสมบูรณ์!")
    print("💡 ขั้นตอนต่อไป:")
    print("   1. แก้ไข FinishLunar.py ให้ใช้ PostgreSQL")
    print("   2. อัปเดต PM2 configuration")
    print("   3. รัน: pm2 restart all")
    
    return True

if __name__ == "__main__":
    main()