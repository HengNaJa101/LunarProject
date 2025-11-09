#!/bin/bash
# Thai Lunar Calendar API - Complete Server Setup Commands
# รันไฟล์นี้บน Linux Server หรือคัดลอกคำสั่งไปรันทีละบรรทัด

echo "🚀 Starting Thai Lunar Calendar API Server Setup..."

# ========================================
# 1. UPDATE REPOSITORY และ DEPENDENCIES
# ========================================

echo "📦 Step 1: Update repository and install dependencies"

# ไปยัง directory โปรเจค
cd /path/to/LunarProject

# ดึงโค้ดล่าสุดจาก GitHub
git pull origin main

# ติดตั้ง Python packages ที่จำเป็น
pip install Flask psycopg2-binary

echo "✅ Repository updated and dependencies installed"

# ========================================
# 2. TEST POSTGRESQL CONNECTION
# ========================================

echo "🔗 Step 2: Testing PostgreSQL connection"

python3 -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='thai_lunar_db',
        user='admin',
        password='p@ssw0rd'
    )
    print('✅ PostgreSQL connection successful!')
    
    # ตรวจสอบตาราง
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM lunar_calendar')
    count = cursor.fetchone()[0]
    print(f'📊 Found {count} records in lunar_calendar table')
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'❌ PostgreSQL connection failed: {e}')
    print('🔧 Please check database setup first!')
    exit(1)
"

# ========================================
# 3. CONFIGURE FIREWALL AND PORTS
# ========================================

echo "🔥 Step 3: Configure firewall and open ports"

# เปิดพอร์ต 8000 สำหรับ API (Ubuntu/Debian)
if command -v ufw >/dev/null 2>&1; then
    echo "Configuring UFW firewall..."
    sudo ufw allow 8000/tcp
    sudo ufw allow ssh
    sudo ufw --force enable
    echo "✅ UFW firewall configured"
elif command -v firewall-cmd >/dev/null 2>&1; then
    echo "Configuring firewalld..."
    sudo firewall-cmd --permanent --add-port=8000/tcp
    sudo firewall-cmd --permanent --add-service=ssh
    sudo firewall-cmd --reload
    echo "✅ Firewalld configured"
else
    echo "⚠️ No firewall detected or manual configuration needed"
    echo "Please open port 8000 manually if needed"
fi

# สร้าง logs directory
mkdir -p logs

echo "✅ Firewall and ports configured"

# ========================================
# 4. START API WITH PM2
# ========================================

echo "🚀 Step 4: Starting API with PM2"

# หยุด process เก่า (ถ้ามี)
pm2 stop thai-lunar-api 2>/dev/null || true
pm2 delete thai-lunar-api 2>/dev/null || true

# เริ่ม API ด้วย PM2
pm2 start ecosystem-api-server.config.js --env production

# บันทึก configuration
pm2 save

# แสดงสถานะ
pm2 status

echo "✅ API started with PM2"

# ========================================
# 4. TEST API ENDPOINTS
# ========================================

echo "🧪 Step 4: Testing API endpoints"

# รอ API เริ่มต้น
sleep 3

echo "Testing /health endpoint:"
curl -s http://localhost:8000/health | python3 -m json.tool

echo -e "\nTesting /usersinfo/get/profile endpoint:"
curl -s http://localhost:8000/usersinfo/get/profile | python3 -m json.tool

echo -e "\nTesting /lunar/today endpoint:"
curl -s http://localhost:8000/lunar/today | python3 -m json.tool

echo -e "\nTesting /lunar/date/2024-11-08 endpoint:"
curl -s http://localhost:8000/lunar/date/2024-11-08 | python3 -m json.tool

echo -e "\nTesting /lunar/stats endpoint:"
curl -s http://localhost:8000/lunar/stats | python3 -m json.tool

# ========================================
# 5. SETUP AUTO-START
# ========================================

echo "⚙️ Step 5: Setup auto-start on boot"

# ตั้งค่า PM2 auto-start
pm2 startup

echo "✅ Auto-start configured"

# ========================================
# 6. SHOW FINAL STATUS
# ========================================

echo "📋 Final Status:"
pm2 status
pm2 logs thai-lunar-api --lines 10

echo ""
echo "🎉 Thai Lunar Calendar API Setup Complete!"
echo ""
echo "📊 API Endpoints:"
echo "   Health Check: http://localhost:8000/health"
echo "   User Profile: http://localhost:8000/usersinfo/get/profile"
echo "   Today Data:   http://localhost:8000/lunar/today"
echo "   Date Query:   http://localhost:8000/lunar/date/YYYY-MM-DD"
echo "   Statistics:   http://localhost:8000/lunar/stats"
echo ""
echo "🔧 Management Commands:"
echo "   pm2 status                    - ดูสถานะ"
echo "   pm2 logs thai-lunar-api       - ดู logs"
echo "   pm2 restart thai-lunar-api    - รีสตาร์ท"
echo "   pm2 stop thai-lunar-api       - หยุด"
echo ""