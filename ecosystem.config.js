module.exports = {
  apps: [{
    name: 'lunar-project',
    script: 'FinishLunar.py',
    interpreter: 'python3',
    cwd: '/path/to/your/project/LunarProject',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};