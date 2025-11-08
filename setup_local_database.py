#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สคริปต์สำหรับสร้าง database และ table ใน PostgreSQL local
"""

import psycopg2
from database_config import LOCAL_DB_CONFIG

def create_database_and_table():
    """สร้าง database และ table สำหรับ thai lunar calendar"""
    
    try:
        print("=== สร้าง Database และ Table ===")
        
        # เชื่อมต่อ default database (postgres)
        conn = psycopg2.connect(**LOCAL_DB_CONFIG)
        conn.autocommit = True  # สำหรับ CREATE DATABASE
        cursor = conn.cursor()
        
        # สร้าง database ใหม่
        database_name = 'thai_lunar_db'
        print(f"📦 กำลังสร้าง database: {database_name}")
        
        # ตรวจสอบว่า database มีอยู่แล้วหรือไม่
        cursor.execute("""
            SELECT 1 FROM pg_database WHERE datname = %s
        """, (database_name,))
        
        if cursor.fetchone():
            print(f"✅ Database {database_name} มีอยู่แล้ว")
        else:
            cursor.execute(f'CREATE DATABASE "{database_name}"')
            print(f"✅ สร้าง Database {database_name} สำเร็จ")
        
        cursor.close()
        conn.close()
        
        # เชื่อมต่อ database ใหม่
        new_config = LOCAL_DB_CONFIG.copy()
        new_config['database'] = database_name
        
        conn = psycopg2.connect(**new_config)
        cursor = conn.cursor()
        
        # สร้าง table สำหรับ lunar calendar
        print("📊 กำลังสร้าง table lunar_calendar")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS lunar_calendar (
            id SERIAL PRIMARY KEY,
            solar_date DATE NOT NULL,
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
        """
        
        cursor.execute(create_table_sql)
        
        # สร้าง index สำหรับการค้นหาที่เร็วขึ้น
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_solar_date 
            ON lunar_calendar(solar_date);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_lunar_date 
            ON lunar_calendar(lunar_year, lunar_month, lunar_day);
        """)
        
        conn.commit()
        print("✅ สร้าง table lunar_calendar สำเร็จ")
        
        # ตรวจสอบ table ที่สร้าง
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"📋 Tables ใน database: {[table[0] for table in tables]}")
        
        cursor.close()
        conn.close()
        
        print("🎯 Database setup เสร็จสมบูรณ์!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def insert_sample_data():
    """ใส่ข้อมูลตัวอย่าง"""
    try:
        config = LOCAL_DB_CONFIG.copy()
        config['database'] = 'thai_lunar_db'
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        print("📝 กำลังใส่ข้อมูลตัวอย่าง...")
        
        sample_data = [
            ('2024-01-01', 2567, 1, 1, 'มกราคม', 'วันจันทร์', 'มะเมีย', 'กบ', False),
            ('2024-02-01', 2567, 2, 1, 'กุมภาพันธ์', 'วันพฤหัสบดี', 'มะเมีย', 'ระกา', False),
            ('2024-03-01', 2567, 3, 1, 'มีนาคม', 'วันศุกร์', 'มะเมีย', 'จอ', False),
        ]
        
        for data in sample_data:
            cursor.execute("""
                INSERT INTO lunar_calendar 
                (solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, 
                 day_name, zodiac_year, zodiac_day, is_leap_month)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, data)
        
        conn.commit()
        
        # ตรวจสอบข้อมูลที่ใส่
        cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        count = cursor.fetchone()[0]
        print(f"📊 มีข้อมูล {count} รายการใน table")
        
        cursor.close()
        conn.close()
        
        print("✅ ใส่ข้อมูลตัวอย่างสำเร็จ!")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setup Local PostgreSQL Database for Thai Lunar Calendar")
    print("=" * 60)
    
    # สร้าง database และ table
    if create_database_and_table():
        # ใส่ข้อมูลตัวอย่าง
        insert_sample_data()
        
        print("\n🎯 การตั้งค่าเสร็จสมบูรณ์!")
        print("💡 ตอนนี้สามารถเปลี่ยนโปรเจ็คให้ใช้ Local Database ได้แล้ว")
    else:
        print("\n❌ การตั้งค่าล้มเหลว")