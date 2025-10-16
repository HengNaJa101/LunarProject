#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thai Lunar Calendar Server - รันบน Port 5433
สำหรับการใช้งานผ่าน Command Line และ Web Interface
"""

import socket
import threading
import json
import sys
import os
from datetime import datetime

# เพิ่ม path สำหรับ import ฟังก์ชันจาก FinishLunar.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from FinishLunar import calculate_thai_lunar_calendar, test_database_connection
except ImportError as e:
    print(f"ไม่สามารถ import ฟังก์ชันจาก FinishLunar.py: {e}")
    sys.exit(1)

class LunarCalendarServer:
    def __init__(self, host='localhost', port=5433):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        """เริ่มต้น server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"🌙 Thai Lunar Calendar Server Started")
            print(f"📡 Host: {self.host}")
            print(f"🔌 Port: {self.port}")
            print(f"🌐 URL: http://{self.host}:{self.port}")
            print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 60)
            print("📝 How to use:")
            print("   - Connect via telnet or netcat")
            print("   - Send JSON format data")
            print("   - Press Ctrl+C to stop server")
            print("-" * 60)
            
            # ทดสอบการเชื่อมต่อฐานข้อมูล
            if test_database_connection():
                print("✅ Database connection successful")
            else:
                print("❌ Cannot connect to database")
                
            print("\n🎯 Waiting for client connections...")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"\n📞 Connection from: {client_address}")
                    
                    # สร้าง thread สำหรับจัดการ client แต่ละตัว
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"❌ ข้อผิดพลาด socket: {e}")
                        
        except Exception as e:
            print(f"❌ ไม่สามารถเริ่ม server ได้: {e}")
            sys.exit(1)
            
    def handle_client(self, client_socket, client_address):
        """จัดการ client connection"""
        try:
            # ส่งข้อความต้อนรับ
            welcome_msg = {
                "status": "connected",
                "message": "🌙 ยินดีต้อนรับสู่ Thai Lunar Calendar Server",
                "instructions": {
                    "format": "JSON",
                    "required_fields": ["birth_year", "birth_month", "birth_day"],
                    "optional_fields": ["pregnancy_months", "time_period"],
                    "example": {
                        "birth_year": 2520,
                        "birth_month": 5,
                        "birth_day": 15,
                        "pregnancy_months": 9,
                        "time_period": "กลางวัน"
                    }
                }
            }
            
            self.send_response(client_socket, welcome_msg)
            
            while True:
                # รับข้อมูลจาก client
                data = client_socket.recv(4096).decode('utf-8').strip()
                
                if not data:
                    break
                    
                if data.lower() in ['exit', 'quit', 'bye']:
                    goodbye_msg = {"status": "disconnected", "message": "👋 ขอบคุณที่ใช้บริการ"}
                    self.send_response(client_socket, goodbye_msg)
                    break
                    
                # ประมวลผลข้อมูลที่ได้รับ
                response = self.process_request(data)
                self.send_response(client_socket, response)
                
        except Exception as e:
            error_msg = {"status": "error", "message": f"ข้อผิดพลาด: {str(e)}"}
            self.send_response(client_socket, error_msg)
            
        finally:
            client_socket.close()
            print(f"📴 Connection closed: {client_address}")
            
    def process_request(self, data):
        """ประมวลผล request จาก client"""
        try:
            # แปลงข้อมูล JSON
            request_data = json.loads(data)
            
            # ตรวจสอบข้อมูลที่จำเป็น
            required_fields = ['birth_year', 'birth_month', 'birth_day']
            for field in required_fields:
                if field not in request_data:
                    return {
                        "status": "error",
                        "message": f"ข้อมูลไม่ครบ: ขาด {field}",
                        "required_fields": required_fields
                    }
            
            # ดึงข้อมูลจาก request
            birth_year = int(request_data['birth_year'])
            birth_month = int(request_data['birth_month'])
            birth_day = int(request_data['birth_day'])
            pregnancy_months = int(request_data.get('pregnancy_months', 9))
            time_period = request_data.get('time_period', 'กลางวัน')
            
            # ตรวจสอบความถูกต้องของข้อมูล
            if not (1 <= birth_month <= 12):
                return {"status": "error", "message": "เดือนต้องอยู่ระหว่าง 1-12"}
                
            if not (1 <= birth_day <= 31):
                return {"status": "error", "message": "วันต้องอยู่ระหว่าง 1-31"}
                
            if not (2400 <= birth_year <= 2600):
                return {"status": "error", "message": "ปีต้องอยู่ระหว่าง 2400-2600"}
            
            # คำนวณข้อมูลจันทรคติ
            print(f"📊 Calculating: {birth_day}/{birth_month}/{birth_year}")
            result = calculate_thai_lunar_calendar(
                birth_year, birth_month, birth_day, 
                pregnancy_months, time_period
            )
            
            return {
                "status": "success",
                "input": {
                    "birth_date": f"{birth_day}/{birth_month}/{birth_year}",
                    "pregnancy_months": pregnancy_months,
                    "time_period": time_period
                },
                "result": result,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "รูปแบบ JSON ไม่ถูกต้อง",
                "example": {
                    "birth_year": 2520,
                    "birth_month": 5,
                    "birth_day": 15,
                    "pregnancy_months": 9,
                    "time_period": "กลางวัน"
                }
            }
            
        except ValueError as e:
            return {"status": "error", "message": f"ข้อมูลไม่ถูกต้อง: {str(e)}"}
            
        except Exception as e:
            return {"status": "error", "message": f"เกิดข้อผิดพลาด: {str(e)}"}
    
    def send_response(self, client_socket, response):
        """ส่งข้อมูลกลับไปยัง client"""
        try:
            response_json = json.dumps(response, ensure_ascii=False, indent=2)
            client_socket.send((response_json + "\n").encode('utf-8'))
        except Exception as e:
            print(f"❌ ไม่สามารถส่งข้อมูลได้: {e}")
    
    def stop_server(self):
        """หยุด server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("\n🛑 Server stopped")

def main():
    """ฟังก์ชันหลัก"""
    print("🌙 Thai Lunar Calendar Server")
    print("=" * 50)
    
    # สร้าง server instance
    server = LunarCalendarServer(host='localhost', port=5433)
    
    try:
        # เริ่ม server
        server.start_server()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Stop signal received (Ctrl+C)")
        server.stop_server()
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        print("👋 Thank you for using our service")

if __name__ == "__main__":
    main()