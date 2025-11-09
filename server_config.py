# -*- coding: utf-8 -*-
"""
Configuration for Remote PostgreSQL Server
ไฟล์ตั้งค่าสำหรับเชื่อมต่อ PostgreSQL บน Server
"""

# =============================================================================
# 🔧 การตั้งค่า Server
# =============================================================================

# IP Address ของ Server ที่มี PostgreSQL
SERVER_IP = "192.168.1.100"  # 👈 เปลี่ยนเป็น IP จริงของ Server

# Port ของ PostgreSQL (ปกติคือ 5432)
POSTGRES_PORT = 5432

# ข้อมูลการเชื่อมต่อฐานข้อมูล
DATABASE_NAME = "thai_lunar_db"
USERNAME = "admin"
PASSWORD = "p@ssw0rd"

# =============================================================================
# 📝 วิธีหา IP Address ของ Server
# =============================================================================
"""
บน Windows Server รัน:
  ipconfig

บน Linux Server รัน:
  ip addr show
  หรือ ifconfig

ตัวอย่าง IP ที่อาจพบ:
- 192.168.1.xxx (Local Network)
- 10.0.0.xxx (Private Network)  
- 172.16.xxx.xxx (Private Network)
- xxx.xxx.xxx.xxx (Public IP)
"""

# =============================================================================
# 🔥 Firewall Settings ที่ต้องตั้งค่าบน Server
# =============================================================================
"""
1. เปิด Port 5432 สำหรับ PostgreSQL:
   Windows Firewall:
   - Control Panel → System and Security → Windows Defender Firewall
   - Advanced Settings → Inbound Rules → New Rule
   - Port → TCP → 5432 → Allow

2. PostgreSQL Configuration:
   แก้ไขไฟล์ postgresql.conf:
   listen_addresses = '*'
   
   แก้ไขไฟล์ pg_hba.conf:
   host all all 0.0.0.0/0 md5
"""

# =============================================================================
# 🧪 การทดสอบการเชื่อมต่อ
# =============================================================================

def get_database_config():
    """ส่งคืน config สำหรับการเชื่อมต่อฐานข้อมูล"""
    return {
        'host': SERVER_IP,
        'port': POSTGRES_PORT,
        'database': DATABASE_NAME,
        'user': USERNAME,
        'password': PASSWORD
    }

def test_connection():
    """ทดสอบการเชื่อมต่อ"""
    try:
        import psycopg2
        config = get_database_config()
        
        print(f"🔍 ทดสอบการเชื่อมต่อไปยัง Server...")
        print(f"   Server IP: {config['host']}")
        print(f"   Port: {config['port']}")
        print(f"   Database: {config['database']}")
        print(f"   User: {config['user']}")
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute('SELECT version()')
        version = cursor.fetchone()
        
        print(f"✅ เชื่อมต่อสำเร็จ!")
        print(f"   PostgreSQL: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ การเชื่อมต่อล้มเหลว: {e}")
        print(f"\nการแก้ไข:")
        print(f"1. ตรวจสอบ IP Address: {SERVER_IP}")
        print(f"2. ตรวจสอบ Firewall บน Server (Port 5432)")
        print(f"3. ตรวจสอบ PostgreSQL Configuration")
        return False

if __name__ == "__main__":
    test_connection()