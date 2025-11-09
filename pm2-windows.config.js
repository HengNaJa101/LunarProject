module.exports = {
  apps: [{
    name: 'thai-lunar-api',
    script: 'api.py',
    interpreter: 'C:\\Python\\python.exe',  // path เต็มของ Python ใน Windows Server
    cwd: 'C:\\LunarProjectNew',  // path ของโปรเจค
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    restart_delay: 2000,
    env: {
      NODE_ENV: 'production',
      FLASK_ENV: 'production',
      PYTHONUNBUFFERED: '1',
      PYTHONIOENCODING: 'utf-8'
    },
    log_file: './logs/api.log',
    out_file: './logs/api-out.log',
    error_file: './logs/api-error.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    merge_logs: true
  }]
}