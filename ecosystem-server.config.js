module.exports = {
  apps: [{
    name: 'lunar-server-5433',
    script: 'lunar_server.py',
    interpreter: 'C:\\Users\\Administrator\\LunarProject\\.venv\\Scripts\\python.exe',
    cwd: 'C:\\Users\\Administrator\\LunarProject',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '512M',
    restart_delay: 4000,
    max_restarts: 10,
    min_uptime: '2s',
    env: {
      NODE_ENV: 'production',
      PM2_HOME: process.env.PM2_HOME || require('os').homedir() + '/.pm2',
      PYTHONUNBUFFERED: '1',
      PYTHONIOENCODING: 'utf-8',
      PYTHONUTF8: '1',
      LANG: 'en_US.UTF-8',
      LC_ALL: 'en_US.UTF-8'
    },
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    out_file: './logs/server-out.log',
    error_file: './logs/server-err.log'
  }]
};