import socket
import sys

def test_port_connection(host='localhost', port=5433):
    """ทดสอบการเชื่อมต่อ port"""
    try:
        print(f"🔍 Testing connection to {host}:{port}")
        
        # สร้าง socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # timeout 5 วินาที
        
        result = sock.connect_ex((host, port))
        
        if result == 0:
            print(f"✅ Port {port} is OPEN on {host}")
            
            # ลองส่งข้อมูลทดสอบ
            try:
                sock.send(b'{"test": "connection"}')
                response = sock.recv(1024)
                print(f"📨 Received response: {response.decode('utf-8')[:100]}...")
            except:
                print("📡 Port is open but no response received")
                
        else:
            print(f"❌ Port {port} is CLOSED or NOT LISTENING on {host}")
            print(f"   Error code: {result}")
            
        sock.close()
        return result == 0
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def check_localhost_addresses():
    """เช็ค localhost addresses"""
    print("\n🌐 Checking localhost addresses:")
    
    addresses = [
        ('localhost', 5433),
        ('127.0.0.1', 5433),
        ('0.0.0.0', 5433),
        ('::1', 5433)  # IPv6 localhost
    ]
    
    for host, port in addresses:
        try:
            print(f"\n📍 Testing {host}:{port}")
            test_port_connection(host, port)
        except Exception as e:
            print(f"❌ Error testing {host}:{port} - {e}")

def scan_common_ports():
    """สแกน port ทั่วไป"""
    print("\n🔍 Scanning common ports on localhost:")
    
    common_ports = [5432, 5433, 8000, 8080, 3000, 5000, 80, 443]
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            
            if result == 0:
                print(f"✅ Port {port} is OPEN")
            else:
                print(f"❌ Port {port} is CLOSED")
                
            sock.close()
        except:
            print(f"❌ Port {port} - Error")

if __name__ == "__main__":
    print("🔍 Thai Lunar Server Port Checker")
    print("=" * 50)
    
    # เช็ค port 5433 หลาย address
    check_localhost_addresses()
    
    # สแกน port อื่นๆ
    scan_common_ports()
    
    print("\n" + "=" * 50)
    print("💡 Tips:")
    print("   - ถ้า port 5433 OPEN = โปรแกรมรันอยู่")
    print("   - ถ้า port 5433 CLOSED = โปรแกรมไม่ได้รัน")
    print("   - ลอง: telnet localhost 5433")
    print("   - หรือ: start_server.bat")