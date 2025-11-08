# Local PostgreSQL Configuration
# สำหรับใช้กับ PostgreSQL ที่ติดตั้งในเครื่อง

import psycopg2

# ข้อมูลการเชื่อมต่อ Local Database
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,  # Port ปกติของ PostgreSQL
    'database': 'thai_lunar_db',  # Database ใหม่ที่สร้างขึ้น
    'user': 'postgres',      # ใช้ user postgres (default)
    'password': 'postgres'   # รหัสผ่าน postgres
}

# ข้อมูลการเชื่อมต่อ Remote Database (เดิม)
REMOTE_DB_CONFIG = {
    'host': 'Chainchinjung.3bbddns.com',
    'port': 57721,
    'database': 'thai-hub',
    'user': 'thaiHub',
    'password': 'your_remote_password'
}

def test_local_database():
    """ทดสอบการเชื่อมต่อ Local Database"""
    try:
        print("=== Testing Local Database Connection ===")
        conn = psycopg2.connect(**LOCAL_DB_CONFIG)
        cursor = conn.cursor()
        
        # ทดสอบ query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Local PostgreSQL Version: {version[0]}")
        
        # ตรวจสอบตาราง
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"📊 Tables in database: {[table[0] for table in tables]}")
        
        cursor.close()
        conn.close()
        print("✅ Local database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Local database connection failed: {e}")
        return False

def test_remote_database():
    """ทดสอบการเชื่อมต่อ Remote Database"""
    try:
        print("=== Testing Remote Database Connection ===")
        conn = psycopg2.connect(**REMOTE_DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Remote PostgreSQL Version: {version[0]}")
        
        cursor.close()
        conn.close()
        print("✅ Remote database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Remote database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Database Connection Test")
    print("=" * 50)
    
    # ทดสอบ Local Database
    local_ok = test_local_database()
    print()
    
    # ทดสอบ Remote Database
    remote_ok = test_remote_database()
    print()
    
    if local_ok:
        print("🎯 แนะนำ: ใช้ Local Database เพื่อความเร็ว")
    elif remote_ok:
        print("🌐 ใช้ Remote Database")
    else:
        print("❌ ไม่สามารถเชื่อมต่อ Database ได้")