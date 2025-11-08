module.exports = {
  apps: [
    {
      name: 'lunar-main',
      script: 'FinishLunar_sqlite.py',
      args: '--pm2',
      interpreter: 'C:\\LunarProjectNew\\.venv\\Scripts\\python.exe',
      cwd: 'C:\\LunarProjectNew',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '512M',
      restart_delay: 2000,
      max_restarts: 10,
      min_uptime: '2s',
      env: {
        NODE_ENV: 'production',
        PM2_HOME: process.env.PM2_HOME || require('os').homedir() + '/.pm2',
        PYTHONUNBUFFERED: '1',
        PYTHONIOENCODING: 'utf-8',
        PYTHONUTF8: '1',
        LANG: 'en_US.UTF-8'
      },
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      out_file: './logs/sqlite-out.log',
      error_file: './logs/sqlite-err.log'
    }
  ]
};