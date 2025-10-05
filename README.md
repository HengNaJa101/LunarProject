pip --versiondir# Thai Lunar Calendar Project

This project provides Thai Lunar Calendar functionality with PostgreSQL database integration.

## Features
- Database connection testing
- Thai lunar calendar data management
- PostgreSQL integration

## Requirements
- Python 3.x
- PostgreSQL database
- Dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HengNaJa101/LunarProject.git
cd LunarProject
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database settings in `FinishLunar.py` if needed.

4. Run the application:
```bash
python FinishLunar.py
```

## PM2 Deployment

### Quick Deploy

For Linux/Mac servers:
```bash
chmod +x deploy.sh
./deploy.sh
```

For Windows servers:
```cmd
deploy.bat
```

### Manual PM2 Commands

1. Start the application:
```bash
pm2 start ecosystem.config.js
```

2. Monitor the application:
```bash
pm2 status
pm2 logs lunar-project
pm2 monit
```

3. Restart/Stop the application:
```bash
pm2 restart lunar-project
pm2 stop lunar-project
```

4. Make PM2 startup on boot:
```bash
pm2 startup
pm2 save
```

### Using npm scripts

You can also use the predefined npm scripts:
```bash
npm run pm2:start    # Start with PM2
npm run pm2:stop     # Stop PM2 process
npm run pm2:restart  # Restart PM2 process
npm run pm2:logs     # View logs
npm run pm2:monit    # Monitor processes
```

## Database Configuration

The application connects to a PostgreSQL database with the following default configuration:
- Host: Chainchinjung.3bbddns.com
- Port: 57721
- Database: thai-hub
- User: thaiHub

Make sure your database is accessible and the table `thai_lunar_calendar` exists.