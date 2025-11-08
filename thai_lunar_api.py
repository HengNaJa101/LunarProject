# -*- coding: utf-8 -*-
"""
Thai Lunar Calendar API with PostgreSQL
สร้าง REST API สำหรับปฏิทินจันทรคติ ใช้ PostgreSQL
"""

from flask import Flask, jsonify, request
import psycopg2
from datetime import datetime, date
import json

app = Flask(__name__)

# การตั้งค่า PostgreSQL
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thai_lunar_db',
    'user': 'postgres',
    'password': '123456'  # รหัสผ่าน PostgreSQL ใน server
}

def get_db_connection():
    """สร้างการเชื่อมต่อ PostgreSQL"""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/usersinfo/get/profile', methods=['GET'])
def get_user_profile():
    """API endpoint เหมือนในรูป - ข้อมูล user profile"""
    
    try:
        # ดึงข้อมูลจาก database
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # ดึงข้อมูลปฏิทินวันนี้
        cursor.execute("""
            SELECT lunar_year, lunar_month, lunar_day, day_name, zodiac_year, zodiac_day
            FROM lunar_calendar 
            WHERE solar_date = CURRENT_DATE
            LIMIT 1
        """)
        
        today_lunar = cursor.fetchone()
        
        if today_lunar:
            lunar_year, lunar_month, lunar_day, day_name, zodiac_year, zodiac_day = today_lunar
        else:
            # ถ้าไม่มีข้อมูลวันนี้ ใช้ข้อมูลล่าสุด
            lunar_year, lunar_month, lunar_day = 2567, 12, 15
            day_name, zodiac_year, zodiac_day = "วันศุกร์", "มะเมีย", "กบ"
        
        # สร้าง response แบบเดียวกับในรูป
        response_data = {
            "id": 21,
            "username": "thai_lunar_user",
            "full_name": f"ปฏิทินจันทรคติ {lunar_year}/{lunar_month}/{lunar_day}",
            "phone_number": f"{lunar_year}{lunar_month:02d}{lunar_day:02d}",
            "lat": f"{lunar_year}.{lunar_month}{lunar_day}",
            "exp": f"{int(datetime.now().timestamp())}"
        }
        
        cursor.close()
        conn.close()
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lunar/today', methods=['GET'])
def get_today_lunar():
    """API สำหรับดึงข้อมูลปฏิทินจันทรคติวันนี้"""
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                solar_date,
                lunar_year,
                lunar_month,
                lunar_day,
                lunar_month_name,
                day_name,
                zodiac_year,
                zodiac_day,
                is_leap_month,
                created_at
            FROM lunar_calendar 
            WHERE solar_date = CURRENT_DATE
        """)
        
        result = cursor.fetchone()
        
        if result:
            solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month, created_at = result
            
            response_data = {
                "solar_date": str(solar_date),
                "lunar_date": {
                    "year": lunar_year,
                    "month": lunar_month,
                    "day": lunar_day,
                    "month_name": lunar_month_name
                },
                "day_info": {
                    "day_name": day_name,
                    "zodiac_year": zodiac_year,
                    "zodiac_day": zodiac_day,
                    "is_leap_month": is_leap_month
                },
                "timestamp": int(datetime.now().timestamp())
            }
        else:
            response_data = {
                "error": "No data found for today",
                "timestamp": int(datetime.now().timestamp())
            }
        
        cursor.close()
        conn.close()
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lunar/date/<date_string>', methods=['GET'])
def get_lunar_by_date(date_string):
    """API สำหรับดึงข้อมูลปฏิทินจันทรคติตามวันที่ (YYYY-MM-DD)"""
    
    try:
        # ตรวจสอบรูปแบบวันที่
        try:
            target_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                solar_date,
                lunar_year,
                lunar_month,
                lunar_day,
                lunar_month_name,
                day_name,
                zodiac_year,
                zodiac_day,
                is_leap_month
            FROM lunar_calendar 
            WHERE solar_date = %s
        """, (target_date,))
        
        result = cursor.fetchone()
        
        if result:
            solar_date, lunar_year, lunar_month, lunar_day, lunar_month_name, day_name, zodiac_year, zodiac_day, is_leap_month = result
            
            response_data = {
                "solar_date": str(solar_date),
                "lunar_date": {
                    "year": lunar_year,
                    "month": lunar_month,
                    "day": lunar_day,
                    "month_name": lunar_month_name
                },
                "day_info": {
                    "day_name": day_name,
                    "zodiac_year": zodiac_year,
                    "zodiac_day": zodiac_day,
                    "is_leap_month": is_leap_month
                },
                "timestamp": int(datetime.now().timestamp())
            }
        else:
            response_data = {
                "error": f"No data found for date {date_string}",
                "timestamp": int(datetime.now().timestamp())
            }
        
        cursor.close()
        conn.close()
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lunar/stats', methods=['GET'])
def get_lunar_stats():
    """API สำหรับดึงสถิติข้อมูลในฐานข้อมูล"""
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # นับจำนวนข้อมูลทั้งหมด
        cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        total_records = cursor.fetchone()[0]
        
        # หาช่วงวันที่
        cursor.execute("""
            SELECT MIN(solar_date), MAX(solar_date) 
            FROM lunar_calendar
        """)
        date_range = cursor.fetchone()
        min_date, max_date = date_range if date_range[0] else (None, None)
        
        # นับตามปี
        cursor.execute("""
            SELECT lunar_year, COUNT(*) 
            FROM lunar_calendar 
            GROUP BY lunar_year 
            ORDER BY lunar_year
        """)
        year_stats = cursor.fetchall()
        
        response_data = {
            "total_records": total_records,
            "date_range": {
                "min_date": str(min_date) if min_date else None,
                "max_date": str(max_date) if max_date else None
            },
            "year_statistics": [
                {"lunar_year": year, "count": count} 
                for year, count in year_stats
            ],
            "timestamp": int(datetime.now().timestamp())
        }
        
        cursor.close()
        conn.close()
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "timestamp": int(datetime.now().timestamp())
            })
        else:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "timestamp": int(datetime.now().timestamp())
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": int(datetime.now().timestamp())
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Thai Lunar Calendar API (PostgreSQL)")
    print("📊 Available endpoints:")
    print("   GET /usersinfo/get/profile  - User profile (ตามรูป)")
    print("   GET /lunar/today            - ข้อมูลวันนี้")
    print("   GET /lunar/date/YYYY-MM-DD  - ข้อมูลตามวันที่")
    print("   GET /lunar/stats            - สถิติข้อมูล")
    print("   GET /health                 - Health check")
    print("🌐 Running on: http://localhost:8000")
    
    app.run(host='0.0.0.0', port=8000, debug=True)