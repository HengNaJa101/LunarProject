import psycopg2
from datetime import datetime
import os
import sys
import signal
import time
import logging

# ตั้งค่า encoding สำหรับ Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ตัวแปรสำหรับควบคุมการทำงาน
running = True

def signal_handler(signum, frame):
    """จัดการ signal สำหรับการหยุดทำงานอย่างสุภาพ"""
    global running
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    running = False

# ลงทะเบียน signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# ข้อมูลการเชื่อมต่อฐานข้อมูล
DB_CONFIG = {
    'host': 'Chainchinjung.3bbddns.com',
    'port': 57721,
    'database': 'thai-hub',
    'user': 'thaiHub',
    'password': 'thaiHubPassword'
}

# Import ฟังก์ชันจาก FinishLunar.py
from FinishLunar import (
    calculate_thai_lunar_calendar, 
    test_database_connection,
    check_psycopg2_installation
)

def get_input_with_default(prompt, default_value=""):
    """รับ input จากผู้ใช้ พร้อม default value"""
    if default_value:
        user_input = input(f"{prompt} [default: {default_value}]: ").strip()
        return user_input if user_input else default_value
    return input(prompt).strip()

def run_interactive_session():
    """รันโปรแกรมแบบ interactive ผ่าน PM2"""
    logger.info("Starting Interactive Lunar Calendar Session...")
    
    # ทดสอบการเชื่อมต่อฐานข้อมูล
    if not test_database_connection():
        logger.error("Database connection failed")
        return False
    
    # ตรวจสอบ psycopg2
    if not check_psycopg2_installation():
        logger.error("psycopg2 check failed")
        return False
    
    session_count = 0
    
    while running:
        try:
            session_count += 1
            logger.info(f"=== Session {session_count} ===")
            
            # รับข้อมูลจากผู้ใช้
            print("\n🌙 ระบบคำนวณจันทรคติไทย")
            print("=" * 50)
            
            # วันที่เกิด
            วัน = get_input_with_default("ป้อนวันที่ (1-31)", "15")
            เดือน = get_input_with_default("ป้อนเดือน (1-12)", "5")  
            ปี = get_input_with_default("ป้อนปี พ.ศ.", "2520")
            
            # อายุครรภ์
            print("\n=== เลือกอายุครรภ์ ===")
            print("9 = คลอดปกติ (9 เดือน)")
            print("8 = ผ่าคลอด (8 เดือน)")  
            print("7 = ผ่าคลอด (7 เดือน)")
            print("0 = จำไม่ได้")
            อายุครรภ์ = get_input_with_default("อายุครรภ์ (7,8,9,0)", "9")
            
            # ช่วงเวลา
            print("\n=== เลือกช่วงเวลาเกิด ===")
            print("1 = กลางวัน (00:00-18:00 น.)")
            print("2 = กลางคืน (18:00-24:00 น.)")
            เวลา_choice = get_input_with_default("ช่วงเวลาเกิด (1,2)", "1")
            
            # แปลงข้อมูล
            try:
                วัน = int(วัน)
                เดือน = int(เดือน)
                ปี = int(ปี)
                อายุครรภ์ = int(อายุครรภ์)
                
                if อายุครรภ์ == 0:
                    อายุครรภ์ = 9
                    
                ช่วงเวลา = "กลางวัน" if int(เวลา_choice) == 1 else "กลางคืน"
                
                # ตรวจสอบค่า
                if not (1 <= วัน <= 31):
                    raise ValueError("วันต้องอยู่ระหว่าง 1-31")
                if not (1 <= เดือน <= 12):
                    raise ValueError("เดือนต้องอยู่ระหว่าง 1-12")
                if not (2400 <= ปี <= 2600):
                    raise ValueError("ปีต้องอยู่ระหว่าง 2400-2600")
                    
            except ValueError as e:
                logger.error(f"ข้อมูลไม่ถูกต้อง: {e}")
                continue
            
            # คำนวณผลลัพธ์
            logger.info(f"คำนวณ: {วัน}/{เดือน}/{ปี}, อายุครรภ์: {อายุครรภ์}, เวลา: {ช่วงเวลา}")
            
            ผลลัพธ์ = calculate_thai_lunar_calendar(ปี, เดือน, วัน, อายุครรภ์, ช่วงเวลา)
            
            print("\n" + "="*60)
            print("ผลการคำนวณ:")
            print("="*60)
            print(ผลลัพธ์)
            print("="*60)
            
            # ถามว่าต้องการคำนวณต่อหรือไม่
            print("\nตัวเลือก:")
            print("1 = คำนวณใหม่")
            print("2 = หยุดโปรแกรม")
            choice = get_input_with_default("เลือก (1,2)", "1")
            
            if choice == "2":
                logger.info("User requested to exit")
                break
                
            # พักเล็กน้อย
            time.sleep(1)
            
        except KeyboardInterrupt:
            logger.info("Received Ctrl+C, shutting down...")
            break
        except Exception as e:
            logger.error(f"Error in session: {e}")
            time.sleep(2)
    
    logger.info("Interactive session ended")
    return True

def run_background_service():
    """รันเป็น background service"""
    logger.info("Starting Background Service Mode...")
    
    # ทดสอบการเชื่อมต่อ
    if not test_database_connection():
        logger.error("Database connection failed")
        return False
    
    if not check_psycopg2_installation():
        logger.error("psycopg2 check failed") 
        return False
    
    logger.info("Service is ready and running...")
    
    # Service loop
    while running:
        try:
            time.sleep(30)  # รอ 30 วินาที
            
            # ทดสอบ DB ทุก 5 นาที
            if int(time.time()) % 300 == 0:
                logger.info("Periodic database check...")
                test_database_connection()
                
        except Exception as e:
            logger.error(f"Service error: {e}")
            time.sleep(5)
    
    logger.info("Background service stopped")
    return True

def is_pm2_mode():
    """ตรวจสอบว่าถูกรันด้วย PM2"""
    return 'PM2_HOME' in os.environ or '--pm2' in sys.argv

def is_interactive_mode():
    """ตรวจสอบว่าต้องการรัน interactive mode"""
    return '--interactive' in sys.argv or '-i' in sys.argv

if __name__ == "__main__":
    logger.info("Thai Lunar Calendar Application Starting...")
    
    try:
        if is_pm2_mode():
            if is_interactive_mode():
                # PM2 Interactive Mode
                logger.info("Starting PM2 Interactive Mode...")
                success = run_interactive_session()
            else:
                # PM2 Background Service Mode
                logger.info("Starting PM2 Background Service Mode...")  
                success = run_background_service()
            
            sys.exit(0 if success else 1)
        else:
            # รันแบบปกติ (non-PM2)
            logger.info("Starting Normal Mode...")
            success = run_interactive_session()
            sys.exit(0 if success else 1)
            
    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)