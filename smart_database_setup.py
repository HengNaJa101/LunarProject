# -*- coding: utf-8 -*-
"""
Smart Database Configuration - รองรับหลายรูปแบบการเชื่อมต่อ
"""

import psycopg2
import getpass
import os

def get_database_config():
    """หาการตั้งค่า database ที่ใช้งานได้"""
    
    # รูปแบบการเชื่อมต่อต่างๆ ที่จะลอง
    configs = [
        # Windows Authentication
        {
            'name': 'Windows Authentication',
            'config': {
                'host': 'localhost',
                'port': 5432,
                'database': 'postgres',
                'user': getpass.getuser()
            }
        },
        # Default postgres password
        {
            'name': 'Default postgres',
            'config': {
                'host': 'localhost', 
                'port': 5432,
                'database': 'postgres',
                'user': 'postgres',
                'password': 'postgres'
            }
        },
        # Empty password
        {
            'name': 'No password',
            'config': {
                'host': 'localhost',
                'port': 5432, 
                'database': 'postgres',
                'user': 'postgres',
                'password': ''
            }
        },
        # Common passwords
        {
            'name': 'Password: admin',
            'config': {
                'host': 'localhost',
                'port': 5432,
                'database': 'postgres', 
                'user': 'postgres',
                'password': 'admin'
            }
        }
    ]
    
    print("🔍 กำลังทดสอบการเชื่อมต่อ...")
    
    for config_info in configs:
        try:
            print(f"   ลอง {config_info['name']}...", end=" ")
            conn = psycopg2.connect(**config_info['config'])
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            cursor.close()
            conn.close()
            print("✅ สำเร็จ!")
            return config_info['config']
            
        except Exception as e:
            print("❌ ล้มเหลว")
            continue
    
    print("❌ ไม่สามารถเชื่อมต่อได้ด้วยวิธีใดๆ")
    return None

def smart_setup_database():
    """Setup database อย่างอัจฉริยะ"""
    
    print("🚀 Smart PostgreSQL Database Setup")
    print("=" * 50)
    
    # หาการตั้งค่าที่ใช้งานได้
    base_config = get_database_config()
    
    if not base_config:
        print("❌ ไม่สามารถเชื่อมต่อ PostgreSQL ได้")
        print("💡 แนะนำ:")
        print("   1. ตรวจสอบว่า PostgreSQL service รันอยู่")
        print("   2. ลองตั้งรหัสผ่านใหม่")
        print("   3. ตรวจสอบ pg_hba.conf")
        return False
    
    try:
        print(f"\n✅ ใช้การตั้งค่า: {base_config}")
        
        # เชื่อมต่อ default database
        conn = psycopg2.connect(**base_config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # สร้าง database ใหม่
        database_name = 'thai_lunar_db'
        print(f"\n📦 กำลังสร้าง database: {database_name}")
        
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
        new_config = base_config.copy()
        new_config['database'] = database_name
        
        conn = psycopg2.connect(**new_config)
        cursor = conn.cursor()
        
        # สร้าง table
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
        conn.commit()
        
        print("✅ สร้าง table lunar_calendar สำเร็จ")
        
        # บันทึกการตั้งค่าที่ใช้งานได้
        print(f"\n💾 บันทึกการตั้งค่าที่ใช้งานได้:")
        for key, value in new_config.items():
            if key != 'password':
                print(f"   {key}: {value}")
            else:
                print(f"   {key}: {'*' * len(str(value)) if value else '(empty)'}")
        
        cursor.close()
        conn.close()
        
        return new_config
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    result = smart_setup_database()
    
    if result:
        print("\n🎯 Database setup เสร็จสมบูรณ์!")
        print("💡 ใช้การตั้งค่านี้ในโปรเจ็คของคุณ")
    else:
        print("\n❌ Database setup ล้มเหลว")