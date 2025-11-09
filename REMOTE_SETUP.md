# 🚀 Remote Database Connection Setup

## 📋 สิ่งที่ต้องทำบน Server

### 1. หา IP Address ของ Server
```bash
# Windows Server
ipconfig

# Linux Server  
ip addr show
```

### 2. ตั้งค่า PostgreSQL Configuration
แก้ไขไฟล์ `postgresql.conf`:
```
listen_addresses = '*'
port = 5432
```

แก้ไขไฟล์ `pg_hba.conf`:
```
# Allow connections from any IP
host    all             all             0.0.0.0/0               md5
```

### 3. เปิด Firewall Port 5432
**Windows Server:**
```
- Control Panel → Windows Defender Firewall
- Advanced Settings → Inbound Rules → New Rule
- Port → TCP → Specific Ports: 5432 → Allow
```

**Linux Server:**
```bash
sudo ufw allow 5432/tcp
# หรือ
sudo iptables -A INPUT -p tcp --dport 5432 -j ACCEPT
```

### 4. Restart PostgreSQL Service
**Windows:**
```
services.msc → PostgreSQL → Restart
```

**Linux:**
```bash
sudo systemctl restart postgresql
```

---

## 🔧 สิ่งที่ต้องทำบนเครื่องคุณ

### 1. อัปเดต Server IP
```bash
# วิธีที่ 1: ใช้ script
update_server_ip.bat 192.168.1.100

# วิธีที่ 2: แก้ไขด้วยมือ
# แก้ไขไฟล์ server_config.py
# เปลี่ยน SERVER_IP = "192.168.1.100"
```

### 2. ทดสอบการเชื่อมต่อ
```bash
python server_config.py
```

### 3. เริ่ม API
```bash
python api.py
```

### 4. ทดสอบ API
```bash
# เปิดเบราว์เซอร์ไป:
http://localhost:8000/health
http://localhost:8000/usersinfo/get/profile
```

---

## 🔍 การแก้ไขปัญหาที่พบบ่อย

### ❌ Connection timeout
- ตรวจสอบ IP Address ถูกต้องหรือไม่
- ตรวจสอบ Firewall บน Server
- ตรวจสอบ Network connectivity: `ping SERVER_IP`

### ❌ Authentication failed
- ตรวจสอบ username/password
- ตรวจสอบ pg_hba.conf configuration

### ❌ Database not found
- สร้างฐานข้อมูล `thai_lunar_db` ใน pgAdmin
- รันไฟล์ `database_setup.sql`

---

## 📊 Network Architecture

```
[คุณ] → API (localhost:8000) → PostgreSQL (SERVER_IP:5432) ← [Server]
```

- **API**: รันบนเครื่องคุณ
- **Database**: รันบน Server
- **Connection**: Remote TCP connection via Internet/LAN