@echo off
REM Deploy script for LunarProject on Windows server

echo 🚀 Starting deployment of LunarProject...

REM Clone or pull latest code
if exist "LunarProject" (
    echo 📥 Updating existing repository...
    cd LunarProject
    git pull origin main
) else (
    echo 📥 Cloning repository...
    git clone https://github.com/HengNaJa101/LunarProject.git
    cd LunarProject
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo 📦 Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Create logs directory
if not exist "logs" mkdir logs

REM Stop existing PM2 process if running
echo 🛑 Stopping existing PM2 processes...
pm2 stop lunar-project 2>nul
pm2 delete lunar-project 2>nul

REM Start with PM2
echo 🔄 Starting application with PM2...
pm2 start ecosystem.config.js

REM Save PM2 process list
pm2 save

echo ✅ Deployment completed successfully!
echo 📊 Check status with: pm2 status
echo 📝 Check logs with: pm2 logs lunar-project

pause