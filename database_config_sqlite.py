# -*- coding: utf-8 -*-
"""
SQLite Alternative Database Configuration
ทางเลือกที่ง่ายกว่าสำหรับ server ที่ไม่มี PostgreSQL
"""

import sqlite3
import os
from datetime import datetime

# การตั้งค่าสำหรับ SQLite
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'thai_lunar.db')

def get_sqlite_connection():
    """สร้างการเชื่อมต่อ SQLite"""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    # กำหนดให้ใช้ Row object สำหรับ cursor
    conn.row_factory = sqlite3.Row
    return conn

def setup_sqlite_database():
    """สร้าง database และ table สำหรับ SQLite"""
    
    print("🗄️ SQLite Database Setup")
    print("=" * 40)
    
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        print(f"📁 Database file: {SQLITE_DB_PATH}")
        
        # สร้าง table lunar_calendar
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
        
        # สร้าง index สำหรับการค้นหาที่เร็วขึ้น
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_solar_date 
            ON lunar_calendar(solar_date)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_lunar_date 
            ON lunar_calendar(lunar_year, lunar_month, lunar_day)
        ''')
        
        conn.commit()
        print("✅ สร้าง table lunar_calendar สำเร็จ")
        
        # ใส่ข้อมูลตัวอย่าง (ถ้ายังไม่มี)
        cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_data = [
                ('2024-01-01', 2567, 1, 1, 'มกราคม', 'วันจันทร์', 'มะเมีย', 'กบ', 0),
                ('2024-02-01', 2567, 2, 1, 'กุมภาพันธ์', 'วันพฤหัสบดี', 'มะเมีย', 'ระกา', 0),
                ('2024-03-01', 2567, 3, 1, 'มีนาคม', 'วันศุกร์', 'มะเมีย', 'จอ', 0),
            ]
            
            cursor.executemany('''
                INSERT INTO lunar_calendar 
                (solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, 
                 day_name, zodiac_year, zodiac_day, is_leap_month)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_data)
            
            conn.commit()
            print("📝 ใส่ข้อมูลตัวอย่าง 3 รายการ")
        
        # ตรวจสอบข้อมูล
        cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        count = cursor.fetchone()[0]
        print(f"📊 มีข้อมูล {count} รายการใน database")
        
        cursor.close()
        conn.close()
        
        print("✅ SQLite database setup เสร็จสิ้น!")
        print(f"📁 ไฟล์ database: {SQLITE_DB_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sqlite_connection():
    """ทดสอบการเชื่อมต่อ SQLite"""
    
    try:
        print("\n🔍 ทดสอบการเชื่อมต่อ SQLite...")
        
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        # ทดสอบ query
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        print(f"✅ SQLite Version: {version}")
        
        # ตรวจสอบ tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tables: {[table[0] for table in tables]}")
        
        # ทดสอบข้อมูล
        cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        count = cursor.fetchone()[0]
        print(f"📊 Records: {count}")
        
        cursor.close()
        conn.close()
        
        print("✅ SQLite connection ทำงานปกติ!")
        return True
        
    except Exception as e:
        print(f"❌ SQLite connection error: {e}")
        return False

# สำหรับใช้แทน psycopg2 ในไฟล์อื่นๆ
class SQLiteAdapter:
    """Adapter สำหรับให้ SQLite ทำงานเหมือน psycopg2"""
    
    def __init__(self):
        self.config = {
            'database_type': 'sqlite',
            'database_path': SQLITE_DB_PATH
        }
    
    def connect(self):
        """สร้างการเชื่อมต่อ"""
        return get_sqlite_connection()
    
    def get_config(self):
        """ได้การตั้งค่า"""
        return self.config

if __name__ == "__main__":
    print("🚀 SQLite Database Setup for Thai Lunar Calendar")
    print("=" * 60)
    
    # Setup database
    if setup_sqlite_database():
        # ทดสอบการเชื่อมต่อ
        test_sqlite_connection()
        
        print("\n🎯 Setup เสร็จสมบูรณ์!")
        print("💡 ใช้ SQLite แทน PostgreSQL")
        print("💡 ไม่ต้องติดตั้งอะไรเพิ่ม")
        print("💡 ไฟล์ database จะอยู่ที่ thai_lunar.db")
    else:
        print("\n❌ Setup ล้มเหลว")