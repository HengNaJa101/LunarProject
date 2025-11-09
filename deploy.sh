#!/bin/bash
# Thai Lunar Calendar API - Server Deployment Script

echo "🌙 Thai Lunar Calendar API - Server Setup"
echo "========================================"

# 1. อัพเดตโค้ดจาก GitHub
echo "📦 Step 1: Update code from GitHub"
git pull origin main
echo "✅ Code updated"

# 2. ติดตั้ง Python dependencies
echo "📦 Step 2: Install Python dependencies"
pip3 install Flask psycopg2-binary
echo "✅ Dependencies installed"

# 3. ทดสอบการเชื่อมต่อฐานข้อมูล
echo "🔗 Step 3: Test database connection"
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
    conn.close()
except Exception as e:
    print(f'❌ PostgreSQL connection failed: {e}')
    exit(1)
"

# 4. สร้าง logs directory
mkdir -p logs

# 5. ตั้งค่า firewall (Ubuntu/Debian)
echo "🔥 Step 4: Configure firewall"
if command -v ufw >/dev/null 2>&1; then
    sudo ufw allow 8000/tcp
    sudo ufw --force enable
    echo "✅ UFW firewall configured for port 8000"
else
    echo "⚠️ Please configure firewall manually to allow port 8000"
fi

# 6. รัน API ด้วย PM2
echo "🚀 Step 5: Deploy API with PM2"
pm2 stop thai-lunar-api 2>/dev/null || true
pm2 delete thai-lunar-api 2>/dev/null || true
pm2 start pm2.config.js --env production
pm2 save
echo "✅ API deployed with PM2"

# 7. แสดงสถานะ
echo "📊 Step 6: Status check"
pm2 status
pm2 logs thai-lunar-api --lines 10

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "🌐 API Endpoints:"
echo "   http://localhost:8000/health"
echo "   http://localhost:8000/usersinfo/get/profile"
echo "   http://localhost:8000/lunar/today"
echo "   http://localhost:8000/lunar/date/2025-11-09"
echo "   http://localhost:8000/lunar/stats"
echo ""
echo "🔧 Management Commands:"
echo "   pm2 status          - ดูสถานะ"
echo "   pm2 logs thai-lunar-api - ดู logs"
echo "   pm2 restart thai-lunar-api - รีสตาร์ท"