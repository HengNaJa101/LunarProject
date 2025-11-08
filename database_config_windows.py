# -*- coding: utf-8 -*-
"""
Database Configuration for Windows Authentication
ใช้ Windows Authentication แทน password
"""

import psycopg2
import getpass
import os

# ข้อมูลการเชื่อมต่อ Local Database (Windows Authentication)
LOCAL_DB_CONFIG_WIN = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',  # เริ่มจาก default database
    'user': getpass.getuser(),  # ใช้ username ปัจจุบัน
    # ไม่ต้องใส่ password สำหรับ Windows Authentication
}

# ข้อมูลการเชื่อมต่อ Local Database (พร้อม database ใหม่)
LOCAL_DB_CONFIG_NEW = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thai_lunar_db',
    'user': getpass.getuser(),
}

def test_windows_auth():
    """ทดสอบการเชื่อมต่อด้วย Windows Authentication"""
    try:
        print("=== ทดสอบ Windows Authentication ===")
        print(f"Current User: {getpass.getuser()}")
        print(f"Host: {LOCAL_DB_CONFIG_WIN['host']}")
        print(f"Port: {LOCAL_DB_CONFIG_WIN['port']}")
        print("กำลังเชื่อมต่อ...")
        
        # เชื่อมต่อด้วย Windows Authentication
        conn = psycopg2.connect(**LOCAL_DB_CONFIG_WIN)
        cursor = conn.cursor()
        
        # ทดสอบ query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL Version: {version[0]}")
        
        # ตรวจสอบ users ที่มี
        cursor.execute("SELECT usename FROM pg_user;")
        users = cursor.fetchall()
        print(f"📋 Users: {[user[0] for user in users]}")
        
        cursor.close()
        conn.close()
        print("✅ Windows Authentication สำเร็จ!")
        return True
        
    except Exception as e:
        print(f"❌ Windows Authentication ล้มเหลว: {e}")
        return False

def create_database_with_windows_auth():
    """สร้าง database ด้วย Windows Authentication"""
    try:
        print("\n=== สร้าง Database ด้วย Windows Authentication ===")
        
        # เชื่อมต่อ default database
        conn = psycopg2.connect(**LOCAL_DB_CONFIG_WIN)
        conn.autocommit = True
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
        conn = psycopg2.connect(**LOCAL_DB_CONFIG_NEW)
        cursor = conn.cursor()
        
        # สร้าง table
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
        conn.commit()
        
        print("✅ สร้าง table lunar_calendar สำเร็จ")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setup PostgreSQL with Windows Authentication")
    print("=" * 60)
    
    # ทดสอบ Windows Authentication
    if test_windows_auth():
        # สร้าง database
        if create_database_with_windows_auth():
            print("\n🎯 Setup เสร็จสมบูรณ์!")
            print(f"💡 ใช้ Windows User: {getpass.getuser()}")
            print("💡 ไม่ต้องใส่รหัสผ่าน")
        else:
            print("\n❌ Setup ล้มเหลว")
    else:
        print("\n❌ ไม่สามารถใช้ Windows Authentication ได้")
        print("💡 ลองใช้รหัสผ่าน postgres แทน")