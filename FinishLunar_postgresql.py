# -*- coding: utf-8 -*-
"""
FinishLunar.py - PostgreSQL Version for Server
ใช้งาน PostgreSQL แทน SQLite
"""

import psycopg2
import os
import sys
from datetime import datetime
import signal
import time
import logging

# ตั้งค่า encoding สำหรับ Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

# ตั้งค่า logging สำหรับ PM2
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ตัวแปรสำหรับควบคุมการทำงาน
running = True

# การตั้งค่า Database - PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thai_lunar_db',
    'user': 'postgres',
    'password': 'postgres'  # แก้ไขเป็นรหัสผ่านจริงของ server
}

def signal_handler(signum, frame):
    """จัดการ signal สำหรับการปิดโปรแกรม"""
    global running
    logger.info(f"📨 ได้รับ signal {signum}")
    logger.info("🔄 กำลังปิดโปรแกรม...")
    running = False

# ลงทะเบียน signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def get_postgresql_connection():
    """สร้างการเชื่อมต่อ PostgreSQL"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def test_database_connection():
    """ทดสอบการเชื่อมต่อฐานข้อมูล PostgreSQL"""
    try:
        logger.info("=== ทดสอบการเชื่อมต่อฐานข้อมูล ===")
        logger.info(f"Host: {DB_CONFIG['host']}")
        logger.info(f"Port: {DB_CONFIG['port']}")
        logger.info(f"Database: {DB_CONFIG['database']}")
        logger.info(f"User: {DB_CONFIG['user']}")
        logger.info("กำลังเชื่อมต่อ...")
        
        # เชื่อมต่อฐานข้อมูล
        conn = get_postgresql_connection()
        cursor = conn.cursor()
        
        logger.info("[OK] เชื่อมต่อฐานข้อมูลสำเร็จ!")
        
        # ทดสอบ query ง่ายๆ
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        logger.info(f"[OK] PostgreSQL Version: {version}")
        
        # ตรวจสอบตาราง
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        logger.info(f"[OK] Tables: {table_names}")
        
        # ตรวจสอบข้อมูลในตาราง lunar_calendar
        if 'lunar_calendar' in table_names:
            cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
            count = cursor.fetchone()[0]
            logger.info(f"[OK] มีข้อมูลในตาราง lunar_calendar: {count} รายการ")
        else:
            logger.warning("[WARNING] ไม่พบตาราง lunar_calendar")
        
        cursor.close()
        conn.close()
        logger.info("[OK] ทดสอบฐานข้อมูลสำเร็จ!")
        return True
        
    except Exception as e:
        logger.error(f"[ERROR] การเชื่อมต่อฐานข้อมูลล้มเหลว: {e}")
        logger.error("💡 แนะนำ:")
        logger.error("   1. ตรวจสอบ PostgreSQL service")
        logger.error("   2. ตั้งรหัสผ่าน postgres")
        logger.error("   3. รัน migrate_to_postgresql.py")
        return False

def calculate_lunar_calendar(solar_date):
    """คำนวณปฏิทินจันทรคติ - ตัวอย่างง่ายๆ"""
    try:
        # นี่คือตัวอย่างการคำนวณ - ในความเป็นจริงจะซับซ้อนกว่านี้
        year = solar_date.year
        lunar_year = year + 543  # แปลงเป็น พ.ศ.
        lunar_month = solar_date.month
        lunar_day = solar_date.day
        
        month_names = [
            "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
            "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        ]
        
        day_names = ["วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์", "วันอาทิตย์"]
        
        lunar_month_name = month_names[lunar_month - 1] if lunar_month <= 12 else "เดือน" + str(lunar_month)
        day_name = day_names[solar_date.weekday()]
        
        return {
            'solar_date': solar_date,
            'lunar_year': lunar_year,
            'lunar_month': lunar_month,
            'lunar_day': lunar_day,
            'lunar_month_name': lunar_month_name,
            'day_name': day_name,
            'zodiac_year': 'มะเมีย',  # ตัวอย่าง
            'zodiac_day': 'กบ',      # ตัวอย่าง
            'is_leap_month': False
        }
        
    except Exception as e:
        logger.error(f"[ERROR] การคำนวณปฏิทินจันทรคติล้มเหลว: {e}")
        return None

def save_lunar_data(lunar_data):
    """บันทึกข้อมูลปฏิทินจันทรคติลงฐานข้อมูล"""
    try:
        conn = get_postgresql_connection()
        cursor = conn.cursor()
        
        # ตรวจสอบว่ามีข้อมูลวันที่นี้แล้วหรือไม่
        cursor.execute("SELECT id FROM lunar_calendar WHERE solar_date = %s", 
                      (lunar_data['solar_date'],))
        
        if cursor.fetchone():
            logger.info(f"ข้อมูลวันที่ {lunar_data['solar_date']} มีอยู่แล้ว")
            return True
        
        # บันทึกข้อมูลใหม่
        cursor.execute("""
            INSERT INTO lunar_calendar 
            (solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name,
             day_name, zodiac_year, zodiac_day, is_leap_month)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            lunar_data['solar_date'],
            lunar_data['lunar_year'],
            lunar_data['lunar_month'],
            lunar_data['lunar_day'],
            lunar_data['lunar_month_name'],
            lunar_data['day_name'],
            lunar_data['zodiac_year'],
            lunar_data['zodiac_day'],
            lunar_data['is_leap_month']
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ บันทึกข้อมูลวันที่ {lunar_data['solar_date']} สำเร็จ")
        return True
        
    except Exception as e:
        logger.error(f"[ERROR] การบันทึกข้อมูลล้มเหลว: {e}")
        return False

def main_lunar_service():
    """บริการหลักของโปรแกรมปฏิทินจันทรคติ"""
    global running
    
    logger.info("🚀 เริ่มต้นบริการปฏิทินจันทรคติ (PostgreSQL)")
    logger.info(f"🗄️ Database: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    
    # ทดสอบการเชื่อมต่อฐานข้อมูล
    if not test_database_connection():
        logger.error("❌ ไม่สามารถเชื่อมต่อฐานข้อมูลได้")
        return
    
    iteration = 0
    
    while running:
        try:
            iteration += 1
            current_time = datetime.now()
            
            logger.info(f"🔄 การทำงานครั้งที่ {iteration} - {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # คำนวณปฏิทินจันทรคติสำหรับวันนี้
            lunar_data = calculate_lunar_calendar(current_time.date())
            
            if lunar_data:
                logger.info(f"📅 ปฏิทินจันทรคติ: {lunar_data['lunar_year']}/{lunar_data['lunar_month']}/{lunar_data['lunar_day']}")
                logger.info(f"🗓️ วัน: {lunar_data['day_name']} เดือน: {lunar_data['lunar_month_name']}")
                
                # บันทึกข้อมูลลงฐานข้อมูล
                save_lunar_data(lunar_data)
            
            # หน่วงเวลา 10 วินาที
            for i in range(10):
                if not running:
                    break
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"[ERROR] เกิดข้อผิดพลาดในการทำงาน: {e}")
            time.sleep(5)
    
    logger.info("✅ บริการปฏิทินจันทรคติหยุดทำงานแล้ว")

if __name__ == "__main__":
    try:
        logger.info("ไฟล์โปรแกรม: " + __file__)
        logger.info("โฟลเดอร์ทำงาน: " + os.getcwd())
        
        # แสดงข้อมูลเวอร์ชัน Python
        logger.info("=== ข้อมูลเวอร์ชัน Python ===")
        logger.info(f"Python Version: {sys.version}")
        logger.info(f"Python Version Info: {sys.version_info}")
        logger.info(f"Python Executable: {sys.executable}")
        logger.info("=" * 50)
        
        # ตรวจสอบ psycopg2
        logger.info("=== ข้อมูลการติดตั้ง psycopg2 ===")
        try:
            import psycopg2
            logger.info(f"psycopg2 Version: {psycopg2.__version__}")
            logger.info(f"psycopg2 Module: {psycopg2.__file__}")
            logger.info("[OK] psycopg2 พร้อมใช้งาน")
        except Exception as e:
            logger.error(f"[ERROR] psycopg2 ไม่พร้อมใช้งาน: {e}")
            
        logger.info("=" * 50)
        
        # ตรวจสอบว่าเป็นการรันผ่าน PM2 หรือไม่
        if len(sys.argv) > 1 and '--pm2' in sys.argv:
            logger.info("🔄 รันผ่าน PM2 - เริ่มบริการ")
            main_lunar_service()
        else:
            logger.info("💡 รันแบบ manual - กด Enter เพื่อปิดโปรแกรม")
            
            # ทดสอบการเชื่อมต่อฐานข้อมูล
            test_database_connection()
            
            # รอให้ผู้ใช้กด Enter
            try:
                input("กด Enter เพื่อปิดโปรแกรม...")
            except KeyboardInterrupt:
                logger.info("\n🔄 ได้รับ Ctrl+C")
            except EOFError:
                logger.info("🔄 ได้รับ EOF")
                
    except Exception as e:
        logger.error(f"[ERROR] เกิดข้อผิดพลาดร้ายแรง: {e}")
        sys.exit(1)