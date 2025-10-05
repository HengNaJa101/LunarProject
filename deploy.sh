#!/bin/bash

# Deploy script for LunarProject on server
echo "🚀 Starting deployment of LunarProject..."

# Clone or pull latest code
if [ -d "LunarProject" ]; then
    echo "📥 Updating existing repository..."
    cd LunarProject
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone https://github.com/HengNaJa101/LunarProject.git
    cd LunarProject
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Update ecosystem.config.js with correct path
echo "⚙️  Updating PM2 configuration..."
CURRENT_PATH=$(pwd)
sed -i "s|/path/to/your/project/LunarProject|$CURRENT_PATH|g" ecosystem.config.js

# Stop existing PM2 process if running
echo "🛑 Stopping existing PM2 processes..."
pm2 stop lunar-project 2>/dev/null || true
pm2 delete lunar-project 2>/dev/null || true

# Start with PM2
echo "🔄 Starting application with PM2..."
pm2 start ecosystem.config.js

# Save PM2 process list
pm2 save

echo "✅ Deployment completed successfully!"
echo "📊 Check status with: pm2 status"
echo "📝 Check logs with: pm2 logs lunar-project"