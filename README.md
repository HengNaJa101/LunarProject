# 🌙 Thai Lunar Calendar API

REST API สำหรับปฏิทินจันทรคติไทย พร้อม PostgreSQL database

## 🚀 Quick Start

### 1. Setup Database
```sql
-- รันใน pgAdmin Query Tool
\i postgresql_setup.sql
```

### 2. Deploy API
```bash
# Linux/Mac
./server_setup.sh

# Windows
server_setup.bat
```

### 3. Test API
```bash
./test_api.sh
```

## 📊 API Endpoints

- **Health Check:** `GET /health`
- **User Profile:** `GET /usersinfo/get/profile`  
- **Today Data:** `GET /lunar/today`
- **Date Query:** `GET /lunar/date/YYYY-MM-DD`
- **Statistics:** `GET /lunar/stats`

## 🛠 Files Structure

### Core Files
- `thai_lunar_api.py` - Main API application
- `postgresql_setup.sql` - Database setup script
- `ecosystem-api.config.js` - PM2 configuration

### Setup Scripts  
- `server_setup.sh/.bat` - Complete server setup
- `test_api.sh` - API testing script

### Legacy Files
- `FinishLunar.py` - Original calculation engine
- `database_config.py` - Database connection utilities

## 🔧 Management Commands

```bash
pm2 status                    # ดูสถานะ
pm2 logs thai-lunar-api       # ดู logs  
pm2 restart thai-lunar-api    # รีสตาร์ท
pm2 stop thai-lunar-api       # หยุด
```

## 📚 Documentation

- `API_README.md` - API documentation
- `PM2_COMPLETE_GUIDE.md` - PM2 management guide
- `SERVER_DEPLOYMENT_COMMANDS.md` - Detailed deployment guide