# -*- coding: utf-8 -*-
"""
Thai Lunar Calendar API
API สำหรับปฏิทินจันทรคติไทย รองรับ PostgreSQL
"""

import os
import sys

# แก้ไขปัญหา encoding ใน Windows - ใช้หลายวิธี
if sys.platform == 'win32':
    # วิธีที่ 1: Environment variables
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    # วิธีที่ 2: Codecs wrapper (สำหรับ Windows Server)
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except Exception:
        pass  # หากใช้ไม่ได้ ให้ใช้ environment variables

from flask import Flask, jsonify, request
import psycopg2
from datetime import datetime, date
import json
import logging

app = Flask(__name__)

# ตั้งค่า logging แบบ UTF-8
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# การตั้งค่า PostgreSQL สำหรับ Server
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thai_lunar_db',
    'user': 'admin',         # ใช้ login user ที่ตั้งค่าไว้
    'password': 'p@ssw0rd'   # รหัสผ่านที่ตั้งค่าไว้
}

def get_database_connection():
    """เชื่อมต่อกับ PostgreSQL database"""
    try:
        connection = psycopg2.connect(**DATABASE_CONFIG)
        return connection
    except Exception as error:
        logger.error(f"Database connection failed: {error}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """ตรวจสอบสถานะ API และการเชื่อมต่อฐานข้อมูล"""
    try:
        # ทดสอบการเชื่อมต่อฐานข้อมูล
        conn = get_database_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "message": "Thai Lunar Calendar API is running",
                "timestamp": int(datetime.now().timestamp())
            }), 200
        else:
            return jsonify({
                "status": "unhealthy", 
                "database": "disconnected",
                "message": "Database connection failed",
                "timestamp": int(datetime.now().timestamp())
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": int(datetime.now().timestamp())
        }), 500

@app.route('/usersinfo/get/profile', methods=['GET'])
def get_user_profile():
    """API endpoint ตามรูปที่ต้องการ - ส่งข้อมูล user profile"""
    try:
        # สร้าง response ตามรูปที่แสดง
        response_data = {
            "id": 21,
            "username": "test1",
            "full_name": "",
            "phone_number": "",
            "lat": "1755502763",
            "exp": str(int(datetime.now().timestamp()))
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in get_user_profile: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/lunar/today', methods=['GET'])
def get_today_lunar():
    """ดึงข้อมูลปฏิทินจันทรคติของวันนี้"""
    try:
        conn = get_database_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # ค้นหาข้อมูลวันนี้
        cursor.execute("""
            SELECT solar_date, lunar_year, lunar_month, lunar_day, 
                   lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month
            FROM lunar_calendar 
            WHERE solar_date = CURRENT_DATE
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        
        if result:
            solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month = result
            
            response_data = {
                "solar_date": str(solar_date),
                "lunar_year": lunar_year,
                "lunar_month": lunar_month, 
                "lunar_day": lunar_day,
                "lunar_month_name": lunar_month_name,
                "day_name": day_name,
                "zodiac_year": zodiac_year,
                "zodiac_day": zodiac_day,
                "is_leap_month": is_leap_month,
                "timestamp": int(datetime.now().timestamp())
            }
        else:
            response_data = {
                "error": "No lunar calendar data found for today",
                "date": str(date.today()),
                "timestamp": int(datetime.now().timestamp())
            }
        
        cursor.close()
        conn.close()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in get_today_lunar: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/lunar/date/<date_string>', methods=['GET'])
def get_lunar_by_date(date_string):
    """ดึงข้อมูลปฏิทินจันทรคติตามวันที่ (รูปแบบ YYYY-MM-DD)"""
    try:
        # ตรวจสอบรูปแบบวันที่
        try:
            target_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        conn = get_database_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT solar_date, lunar_year, lunar_month, lunar_day,
                   lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month
            FROM lunar_calendar 
            WHERE solar_date = %s
        """, (target_date,))
        
        result = cursor.fetchone()
        
        if result:
            solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month = result
            
            response_data = {
                "solar_date": str(solar_date),
                "lunar_year": lunar_year,
                "lunar_month": lunar_month,
                "lunar_day": lunar_day, 
                "lunar_month_name": lunar_month_name,
                "day_name": day_name,
                "zodiac_year": zodiac_year,
                "zodiac_day": zodiac_day,
                "is_leap_month": is_leap_month,
                "timestamp": int(datetime.now().timestamp())
            }
        else:
            response_data = {
                "error": f"No lunar calendar data found for {date_string}",
                "requested_date": date_string,
                "timestamp": int(datetime.now().timestamp())
            }
        
        cursor.close()
        conn.close()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in get_lunar_by_date: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/lunar/stats', methods=['GET'])
def get_lunar_stats():
    """ดึงสถิติข้อมูลในฐานข้อมูล"""
    try:
        conn = get_database_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # นับจำนวนข้อมูลทั้งหมด
        cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        total_records = cursor.fetchone()[0]
        
        # หาช่วงวันที่
        cursor.execute("SELECT MIN(solar_date), MAX(solar_date) FROM lunar_calendar")
        date_range = cursor.fetchone()
        min_date, max_date = date_range
        
        response_data = {
            "total_records": total_records,
            "date_range": {
                "start_date": str(min_date) if min_date else None,
                "end_date": str(max_date) if max_date else None
            },
            "timestamp": int(datetime.now().timestamp())
        }
        
        cursor.close()
        conn.close()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in get_lunar_stats: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # ตั้งค่า environment variables สำหรับ UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    print("Thai Lunar Calendar API Starting...")
    print("Available endpoints:")
    print("   GET /health                   - Health check")
    print("   GET /usersinfo/get/profile    - User profile")
    print("   GET /lunar/today              - Today lunar data")
    print("   GET /lunar/date/YYYY-MM-DD    - Lunar data by date")
    print("   GET /lunar/stats              - Database statistics")
    print("Server running on: http://0.0.0.0:8000")
    
    # รัน Flask app
    app.run(host='0.0.0.0', port=8000, debug=False)