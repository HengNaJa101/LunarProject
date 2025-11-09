module.exports = {
  apps: [{
    name: 'thai-lunar-api-safe',
    script: 'api.py',  // ใช้ไฟล์เดียวกัน แต่ต่าง config
    interpreter: 'python',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env_production: {
      NODE_ENV: 'production', 
      FLASK_ENV: 'production',
      PYTHONUNBUFFERED: '1',
      PYTHONIOENCODING: 'utf-8'
    },
    log_file: './logs/api.log',
    out_file: './logs/api-out.log',
    error_file: './logs/api-error.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss'
  }]
}