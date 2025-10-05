from flask import Flask, request, jsonify
from FinishLunar import calculate_thai_lunar_calendar
import os
import sys

app = Flask(__name__)

@app.route('/lunar', methods=['POST'])
def calculate_lunar():
    """
    API endpoint สำหรับคำนวณจันทรคติไทย
    
    POST data:
    {
        "birth_year": 2520,
        "birth_month": 5,
        "birth_day": 15,
        "pregnancy_months": 9,
        "time_period": "กลางวัน"
    }
    """
    try:
        data = request.get_json()
        
        birth_year = data.get('birth_year')
        birth_month = data.get('birth_month')
        birth_day = data.get('birth_day')
        pregnancy_months = data.get('pregnancy_months', 9)
        time_period = data.get('time_period', 'กลางวัน')
        
        # คำนวณข้อมูลจันทรคติ
        result = calculate_thai_lunar_calendar(
            birth_year, birth_month, birth_day, 
            pregnancy_months, time_period
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/health', methods=['GET'])
def health_check():
    """ตรวจสอบสถานะ API"""
    return jsonify({
        'status': 'healthy',
        'service': 'Thai Lunar Calendar API'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)