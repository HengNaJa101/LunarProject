# Thai Lunar Calendar API - คำสั่งทดสอบ API ทั้งหมด
# Test Commands สำหรับรันบน Server

echo "🧪 Testing Thai Lunar Calendar API"
echo "======================================"

# ตรวจสอบ API server ทำงานหรือไม่
echo "1. Health Check:"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""

# ทดสอบ endpoint หลัก
echo "2. User Profile (ตามรูปที่ต้องการ):"
curl -s http://localhost:8000/usersinfo/get/profile | python3 -m json.tool
echo ""

echo "3. ข้อมูลจันทรคติวันนี้:"
curl -s http://localhost:8000/lunar/today | python3 -m json.tool
echo ""

echo "4. ข้อมูลจันทรคติวันที่ 8 พฤศจิกายน 2024:"
curl -s http://localhost:8000/lunar/date/2024-11-08 | python3 -m json.tool
echo ""

echo "5. ข้อมูลจันทรคติวันที่ 1 มกราคม 2024:"
curl -s http://localhost:8000/lunar/date/2024-01-01 | python3 -m json.tool
echo ""

echo "6. ข้อมูลจันทรคติวันที่ 8 พฤศจิกายน 2025:"
curl -s http://localhost:8000/lunar/date/2025-11-08 | python3 -m json.tool
echo ""

echo "7. สถิติข้อมูลในฐานข้อมูล:"
curl -s http://localhost:8000/lunar/stats | python3 -m json.tool
echo ""

# ทดสอบ error handling
echo "8. ทดสอบ Error Handling (วันที่ผิดรูปแบบ):"
curl -s http://localhost:8000/lunar/date/invalid-date | python3 -m json.tool
echo ""

echo "9. ทดสอบวันที่ไม่มีข้อมูล:"
curl -s http://localhost:8000/lunar/date/2030-01-01 | python3 -m json.tool
echo ""

echo "======================================"
echo "✅ API Testing Complete!"

# แสดงสถานะ PM2
echo ""
echo "📊 PM2 Status:"
pm2 status

echo ""
echo "📋 Recent Logs:"
pm2 logs thai-lunar-api --lines 5