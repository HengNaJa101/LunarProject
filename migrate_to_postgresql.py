# -*- coding: utf-8 -*-
"""
Migrate from SQLite to PostgreSQL 16
ย้ายข้อมูลจาก SQLite ไป PostgreSQL บน server
"""

import sqlite3
import psycopg2
import os
from datetime import datetime

# การตั้งค่า SQLite (source)
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'thai_lunar.db')

# การตั้งค่า PostgreSQL 16 (destination)
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thai_lunar_db',
    'user': 'postgres',
    'password': 'postgres'  # เปลี่ยนเป็นรหัสผ่านจริงของ server
}

def test_postgresql_connection():
    """ทดสอบการเชื่อมต่อ PostgreSQL"""
    try:
        print("🔍 ทดสอบการเชื่อมต่อ PostgreSQL...")
        
        # ลองเชื่อมต่อ default database ก่อน
        default_config = POSTGRES_CONFIG.copy()
        default_config['database'] = 'postgres'
        
        conn = psycopg2.connect(**default_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL Version: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("💡 แนะนำ:")
        print("   1. ตรวจสอบ PostgreSQL service")
        print("   2. ตั้งรหัสผ่าน postgres")
        print("   3. แก้ไข POSTGRES_CONFIG ในไฟล์นี้")
        return False

def create_postgresql_database():
    """สร้าง database ใน PostgreSQL"""
    try:
        print("📦 สร้าง database ใน PostgreSQL...")
        
        # เชื่อมต่อ default database
        default_config = POSTGRES_CONFIG.copy()
        default_config['database'] = 'postgres'
        
        conn = psycopg2.connect(**default_config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # ตรวจสอบว่า database มีอยู่แล้วหรือไม่
        cursor.execute("""
            SELECT 1 FROM pg_database WHERE datname = %s
        """, (POSTGRES_CONFIG['database'],))
        
        if cursor.fetchone():
            print(f"✅ Database '{POSTGRES_CONFIG['database']}' มีอยู่แล้ว")
        else:
            cursor.execute(f'CREATE DATABASE "{POSTGRES_CONFIG['database']}"')
            print(f"✅ สร้าง database '{POSTGRES_CONFIG['database']}' สำเร็จ")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_postgresql_tables():
    """สร้าง tables ใน PostgreSQL"""
    try:
        print("📊 สร้าง tables ใน PostgreSQL...")
        
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        
        # สร้าง table lunar_calendar
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
        
        # สร้าง indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_solar_date 
            ON lunar_calendar(solar_date);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_lunar_date 
            ON lunar_calendar(lunar_year, lunar_month, lunar_day);
        """)
        
        conn.commit()
        print("✅ สร้าง tables และ indexes สำเร็จ")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def migrate_data():
    """ย้ายข้อมูลจาก SQLite ไป PostgreSQL"""
    try:
        print("🔄 ย้ายข้อมูลจาก SQLite ไป PostgreSQL...")
        
        # ตรวจสอบ SQLite
        if not os.path.exists(SQLITE_DB_PATH):
            print(f"⚠️ ไม่พบ SQLite database: {SQLITE_DB_PATH}")
            print("💡 รัน database_config_sqlite.py ก่อน")
            return False
        
        # เชื่อมต่อ SQLite
        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        # เชื่อมต่อ PostgreSQL
        pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
        pg_cursor = pg_conn.cursor()
        
        # อ่านข้อมูลจาก SQLite
        sqlite_cursor.execute("SELECT * FROM lunar_calendar")
        rows = sqlite_cursor.fetchall()
        
        print(f"📊 พบข้อมูล {len(rows)} รายการใน SQLite")
        
        if len(rows) == 0:
            print("⚠️ ไม่มีข้อมูลให้ย้าย")
            return True
        
        # ย้ายข้อมูลไป PostgreSQL
        migrated_count = 0
        
        for row in rows:
            try:
                # ตรวจสอบว่ามีข้อมูลนี้แล้วหรือไม่
                pg_cursor.execute(
                    "SELECT id FROM lunar_calendar WHERE solar_date = %s",
                    (row['solar_date'],)
                )
                
                if pg_cursor.fetchone():
                    continue  # มีข้อมูลแล้ว ข้ามไป
                
                # Insert ข้อมูลใหม่
                pg_cursor.execute("""
                    INSERT INTO lunar_calendar 
                    (solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name,
                     day_name, zodiac_year, zodiac_day, is_leap_month)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        
        # ตรวจสอบข้อมูลใน PostgreSQL
        pg_cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        total_count = pg_cursor.fetchone()[0]
        
        print(f"✅ ย้ายข้อมูล {migrated_count} รายการสำเร็จ")
        print(f"📊 รวมข้อมูลใน PostgreSQL: {total_count} รายการ")
        
        # ปิดการเชื่อมต่อ
        sqlite_cursor.close()
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error migrating data: {e}")
        return False

def update_project_config():
    """อัปเดตการตั้งค่าโปรเจ็คให้ใช้ PostgreSQL"""
    try:
        print("⚙️ อัปเดตการตั้งค่าโปรเจ็ค...")
        
        # สร้างไฟล์ database_config_postgresql.py
        pg_config_content = f'''# -*- coding: utf-8 -*-
"""
PostgreSQL Database Configuration for Server
การตั้งค่า PostgreSQL สำหรับ server
"""

import psycopg2

# การตั้งค่า PostgreSQL บน Server
POSTGRES_CONFIG = {{
    'host': '{POSTGRES_CONFIG['host']}',
    'port': {POSTGRES_CONFIG['port']},
    'database': '{POSTGRES_CONFIG['database']}',
    'user': '{POSTGRES_CONFIG['user']}',
    'password': '{POSTGRES_CONFIG['password']}'
}}

def get_postgresql_connection():
    """สร้างการเชื่อมต่อ PostgreSQL"""
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    return conn

def test_postgresql_connection():
    """ทดสอบการเชื่อมต่อ PostgreSQL"""
    try:
        print("🔍 ทดสอบการเชื่อมต่อ PostgreSQL...")
        
        conn = get_postgresql_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL Version: {{version}}")
        
        cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        count = cursor.fetchone()[0]
        print(f"📊 Records in lunar_calendar: {{count}}")
        
        cursor.close()
        conn.close()
        
        print("✅ PostgreSQL connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {{e}}")
        return False

if __name__ == "__main__":
    test_postgresql_connection()
'''
        
        with open('database_config_postgresql.py', 'w', encoding='utf-8') as f:
            f.write(pg_config_content)
        
        print("✅ สร้างไฟล์ database_config_postgresql.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 SQLite to PostgreSQL Migration")
    print("=" * 60)
    
    # 1. ทดสอบ PostgreSQL
    if not test_postgresql_connection():
        return False
    
    # 2. สร้าง database
    if not create_postgresql_database():
        return False
    
    # 3. สร้าง tables
    if not create_postgresql_tables():
        return False
    
    # 4. ย้ายข้อมูล
    if not migrate_data():
        return False
    
    # 5. อัปเดตการตั้งค่า
    if not update_project_config():
        return False
    
    print("\n🎯 Migration เสร็จสมบูรณ์!")
    print("💡 ขั้นตอนต่อไป:")
    print("   1. แก้ไข FinishLunar.py ให้ใช้ PostgreSQL")
    print("   2. รัน: pm2 restart all")
    print("   3. ตรวจสอบ: pm2 logs")
    
    return True

if __name__ == "__main__":
    main()