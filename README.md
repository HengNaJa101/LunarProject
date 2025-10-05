# Thai Lunar Calendar Project

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

For server deployment with PM2, use the ecosystem configuration file:

```bash
pm2 start ecosystem.config.js
```

## Database Configuration

The application connects to a PostgreSQL database with the following default configuration:
- Host: Chainchinjung.3bbddns.com
- Port: 57721
- Database: thai-hub
- User: thaiHub

Make sure your database is accessible and the table `thai_lunar_calendar` exists.