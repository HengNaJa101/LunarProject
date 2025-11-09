# 🌙 Thai Lunar Calendar API

สมบูรณ์แบบสำหรับ REST API ของปฏิทินจันทรคติไทย

## 🚀 Quick Deploy

### 1. Setup Database
```sql
-- รันใน pgAdmin Query Tool
\i database_setup.sql
```

### 2. Deploy to Server
```bash
./deploy.sh
```

## 📊 API Endpoints

- **Health Check:** `GET /health`
- **User Profile:** `GET /usersinfo/get/profile`  
- **Today Data:** `GET /lunar/today`
- **Date Query:** `GET /lunar/date/YYYY-MM-DD`
- **Statistics:** `GET /lunar/stats`

## � Project Files

- `api.py` - Main API application
- `database_setup.sql` - Database schema and sample data
- `pm2.config.js` - PM2 process manager configuration
- `deploy.sh` - One-click deployment script

## 🔧 Server Management

```bash
pm2 status                  # ดูสถานะ
pm2 logs thai-lunar-api     # ดู logs  
pm2 restart thai-lunar-api  # รีสตาร์ท
pm2 stop thai-lunar-api     # หยุด
```

## 🌐 External Access

API จะรันที่พอร์ต 8000 และสามารถเข้าถึงได้จากภายนอก:
- `http://your-server-ip:8000/health`
- `http://your-server-ip:8000/usersinfo/get/profile`

## 📋 Requirements

- Python 3.7+
- PostgreSQL 12+
- PM2 (Node.js process manager)

## 🔒 Database Configuration

แก้ไขการตั้งค่าใน `api.py`:
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'password': 'your-password'  # เปลี่ยนตามรหัสผ่านจริง
}
```