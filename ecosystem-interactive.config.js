module.exports = {
  apps: [
    // Background Service (ตัวเดิม)
    {
      name: 'lunar-service',
      script: 'FinishLunar.py',
      args: '--pm2',
      interpreter: 'C:\LunarProjectNew\\.venv\\Scripts\\python.exe',
      cwd: 'C:\LunarProjectNew',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '512M',
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
      out_file: './logs/service-out.log',
      error_file: './logs/service-err.log'
    },
    
    // Interactive Mode (ใหม่)
    {
      name: 'lunar-interactive',
      script: 'interactive_lunar.py',
      args: '--pm2 --interactive',
      interpreter: 'C:\LunarProjectNew\\.venv\\Scripts\\python.exe',
      cwd: 'C:\LunarProjectNew',
      instances: 1,
      autorestart: false,  // ไม่รีสตาร์ทอัตโนมัติ
      watch: false,
      max_memory_restart: '256M',
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
      out_file: './logs/interactive-out.log',
      error_file: './logs/interactive-err.log'
    },
    
    // Web API
    {
      name: 'lunar-web-api',
      script: 'web_api.py',
      interpreter: 'C:\LunarProjectNew\\.venv\\Scripts\\python.exe',
      cwd: 'C:\LunarProjectNew',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '512M',
      env: {
        NODE_ENV: 'production',
        FLASK_ENV: 'production',
        PM2_HOME: process.env.PM2_HOME || require('os').homedir() + '/.pm2',
        PYTHONUNBUFFERED: '1',
        PYTHONIOENCODING: 'utf-8',
        PYTHONUTF8: '1'
      },
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      out_file: './logs/web-out.log',
      error_file: './logs/web-err.log'
    }
  ]
};