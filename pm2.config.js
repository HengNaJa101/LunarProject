module.exports = {
  apps: [{
    name: 'thai-lunar-api',
    script: 'api.py',
    interpreter: 'python',  // เปลี่ยนจาก python3 เป็น python
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'development',
      FLASK_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production', 
      FLASK_ENV: 'production'
    },
    log_file: './logs/api.log',
    out_file: './logs/api-out.log',
    error_file: './logs/api-error.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss'
  }]
}