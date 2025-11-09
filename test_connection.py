# -*- coding: utf-8 -*-
"""
ทดสอบการเชื่อมต่อ PostgreSQL ด้วย user admin
"""
import psycopg2
import sys

# การตั้งค่าที่ตรงกับ server
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thai_lunar_db',
    'user': 'admin',
    'password': 'p@ssw0rd'
}

def test_connection():
    """ทดสอบการเชื่อมต่อฐานข้อมูล"""
    try:
        print("🔍 กำลังทดสอบการเชื่อมต่อ PostgreSQL...")
        print(f"   Host: {DATABASE_CONFIG['host']}")
        print(f"   Port: {DATABASE_CONFIG['port']}")
        print(f"   Database: {DATABASE_CONFIG['database']}")
        print(f"   User: {DATABASE_CONFIG['user']}")
        
        # เชื่อมต่อ
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        # ตรวจสอบ version
        cursor.execute('SELECT version()')
        version = cursor.fetchone()
        print(f"✅ เชื่อมต่อสำเร็จ!")
        print(f"   PostgreSQL Version: {version[0]}")
        
        # ตรวจสอบฐานข้อมูล
        cursor.execute("SELECT current_database()")
        db_name = cursor.fetchone()[0]
        print(f"   Current Database: {db_name}")
        
        # ตรวจสอบตาราง
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"   ตารางที่มีอยู่: {len(tables)} ตาราง")
            for table in tables:
                print(f"     - {table[0]}")
                
            # ถ้ามี lunar_calendar ให้ตรวจสอบข้อมูล
            table_names = [table[0] for table in tables]
            if 'lunar_calendar' in table_names:
                cursor.execute('SELECT COUNT(*) FROM lunar_calendar')
                count = cursor.fetchone()[0]
                print(f"   ข้อมูลใน lunar_calendar: {count} records")
            else:
                print("   ⚠️  ยังไม่มีตาราง lunar_calendar")
        else:
            print("   ⚠️  ยังไม่มีตารางใดๆ ในฐานข้อมูล")
        
        cursor.close()
        conn.close()
        print("\n🎉 การทดสอบเสร็จสิ้น!")
        return True
        
    except Exception as e:
        print(f"❌ การเชื่อมต่อล้มเหลว: {e}")
        print("\nการแก้ไข:")
        print("1. ตรวจสอบว่า PostgreSQL เริ่มต้นแล้ว")
        print("2. ตรวจสอบ username/password ใน pgAdmin")
        print("3. ตรวจสอบว่าฐานข้อมูล 'thai_lunar_db' มีอยู่")
        return False

if __name__ == "__main__":
    test_connection()