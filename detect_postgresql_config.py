# -*- coding: utf-8 -*-
"""
Smart PostgreSQL Configuration Detective
หาการตั้งค่า PostgreSQL ที่ใช้งานได้อัตโนมัติ
"""

import psycopg2
import getpass
import os

def try_postgresql_configs():
    """ลองการตั้งค่า PostgreSQL หลายแบบ"""
    
    # การตั้งค่าที่เป็นไปได้
    configs = [
        # Windows Authentication
        {
            'name': 'Windows Authentication',
            'config': {
                'host': 'localhost',
                'port': 5432,
                'database': 'postgres',
                'user': getpass.getuser()
                # ไม่ต้องใส่ password
            }
        },
        # รหัสผ่าน postgres
        {
            'name': 'Default postgres/postgres',
            'config': {
                'host': 'localhost',
                'port': 5432,
                'database': 'postgres',
                'user': 'postgres',
                'password': 'postgres'
            }
        },
        # ไม่มีรหัสผ่าน
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
        # รหัสผ่านที่เป็นไปได้อื่นๆ
        {
            'name': 'Password: admin',
            'config': {
                'host': 'localhost',
                'port': 5432,
                'database': 'postgres',
                'user': 'postgres',
                'password': 'admin'
            }
        },
        {
            'name': 'Password: 123456',
            'config': {
                'host': 'localhost',
                'port': 5432,
                'database': 'postgres',
                'user': 'postgres',
                'password': '123456'
            }
        },
        {
            'name': 'Password: root',
            'config': {
                'host': 'localhost',
                'port': 5432,
                'database': 'postgres',
                'user': 'postgres',
                'password': 'root'
            }
        }
    ]
    
    print("🔍 กำลังทดสอบการเชื่อมต่อ PostgreSQL...")
    print("-" * 50)
    
    for config_info in configs:
        try:
            print(f"   🔐 ลอง {config_info['name']}...", end=" ")
            
            conn = psycopg2.connect(**config_info['config'])
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            print("✅ สำเร็จ!")
            print(f"   📋 การตั้งค่าที่ใช้งานได้:")
            for key, value in config_info['config'].items():
                if key != 'password':
                    print(f"      {key}: {value}")
                else:
                    print(f"      {key}: {'*' * len(str(value)) if value else '(empty)'}")
            
            print(f"   🗄️ PostgreSQL Version: {version[:50]}...")
            return config_info['config']
            
        except Exception as e:
            print("❌ ล้มเหลว")
            print(f"      Error: {str(e)[:80]}...")
            continue
    
    print("\n❌ ไม่สามารถเชื่อมต่อได้ด้วยการตั้งค่าใดๆ")
    return None

def create_working_config_file(working_config):
    """สร้างไฟล์การตั้งค่าที่ใช้งานได้"""
    
    config_content = f'''# -*- coding: utf-8 -*-
"""
Working PostgreSQL Configuration
การตั้งค่า PostgreSQL ที่ทำงานได้จริงบน server นี้
"""

import psycopg2

# การตั้งค่าที่ทำงานได้
POSTGRES_CONFIG = {working_config}

def get_postgresql_connection():
    """สร้างการเชื่อมต่อ PostgreSQL"""
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    return conn

def test_connection():
    """ทดสอบการเชื่อมต่อ"""
    try:
        conn = get_postgresql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL Version: {{version}}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {{e}}")
        return False

if __name__ == "__main__":
    test_connection()
'''
    
    with open('postgresql_working_config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"\n💾 สร้างไฟล์ postgresql_working_config.py")
    print("💡 ไฟล์นี้มีการตั้งค่าที่ใช้งานได้จริง")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 PostgreSQL Configuration Detective")
    print("=" * 60)
    
    # หาการตั้งค่าที่ใช้งานได้
    working_config = try_postgresql_configs()
    
    if working_config:
        print("\n🎯 พบการตั้งค่าที่ใช้งานได้!")
        
        # สร้างไฟล์การตั้งค่า
        create_working_config_file(working_config)
        
        print("\n📋 ขั้นตอนต่อไป:")
        print("   1. ใช้การตั้งค่าข้างต้นใน migrate_to_postgresql.py")
        print("   2. ใช้การตั้งค่าข้างต้นใน FinishLunar_postgresql.py")
        print("   3. รัน: python migrate_to_postgresql.py")
        
        return working_config
    else:
        print("\n❌ ไม่พบการตั้งค่าที่ใช้งานได้")
        print("\n💡 วิธีแก้ไข:")
        print("   1. ตรวจสอบ PostgreSQL service: sc query postgresql-x64-16")
        print("   2. รีเซ็ตรหัสผ่าน: รัน fix_postgresql_password.bat")
        print("   3. แก้ไข pg_hba.conf ให้ใช้ trust authentication")
        print("   4. ใช้ SQLite แทน: pm2 start ecosystem-sqlite.config.js")
        
        return None

if __name__ == "__main__":
    main()