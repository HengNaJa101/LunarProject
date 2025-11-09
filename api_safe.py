# -*- coding: utf-8 -*-
"""
Thai Lunar Calendar API - English Version
Simple API for Thai Lunar Calendar with PostgreSQL
"""

import os
import sys

# Fix Windows encoding issues
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUNBUFFERED'] = '1'

from flask import Flask, jsonify, request
import psycopg2
from datetime import datetime, date
import json
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# PostgreSQL Configuration for Server
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'thai_lunar_db',
    'user': 'postgres', 
    'password': '123456'
}

def get_database_connection():
    """Connect to PostgreSQL database"""
    try:
        connection = psycopg2.connect(**DATABASE_CONFIG)
        return connection
    except Exception as error:
        logger.error(f"Database connection failed: {error}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Check API and database status"""
    try:
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
    """User profile endpoint as per requirements"""
    try:
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
    """Get today's lunar calendar data"""
    try:
        conn = get_database_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
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
    """Get lunar calendar data by date (YYYY-MM-DD format)"""
    try:
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
    """Get database statistics"""
    try:
        conn = get_database_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM lunar_calendar")
        total_records = cursor.fetchone()[0]
        
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
    print("Thai Lunar Calendar API Starting...")
    print("Available endpoints:")
    print("   GET /health                   - Health check")
    print("   GET /usersinfo/get/profile    - User profile")
    print("   GET /lunar/today              - Today lunar data")
    print("   GET /lunar/date/YYYY-MM-DD    - Lunar data by date")
    print("   GET /lunar/stats              - Database statistics")
    print("Server running on: http://0.0.0.0:8000")
    
    app.run(host='0.0.0.0', port=8000, debug=False)