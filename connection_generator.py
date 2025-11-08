#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thai Lunar Calendar - Connection URL Generator
Generate PostgreSQL connection URLs for different configurations
"""

import json
from urllib.parse import quote_plus

class ConnectionURLGenerator:
    """สำหรับสร้าง PostgreSQL connection URLs"""
    
    def __init__(self):
        self.configs = {
            'local': {
                'host': 'localhost',
                'port': 5432,
                'database': 'thai_lunar_db',
                'username': 'postgres',
                'password': 'postgres'
            },
            'remote': {
                'host': 'Chainchinjung.3bbddns.com',
                'port': 57721,
                'database': 'thai-hub',
                'username': 'thaiHub', 
                'password': 'your_remote_password'
            },
            'server': {
                'host': 'localhost',
                'port': 5433,
                'database': 'thai-hub-local',
                'username': 'thaiHub',
                'password': 'your_password_here'
            }
        }
    
    def generate_url(self, config_name, custom_password=None):
        """สร้าง PostgreSQL URL"""
        if config_name not in self.configs:
            return f"Error: Unknown config '{config_name}'"
            
        config = self.configs[config_name].copy()
        
        if custom_password:
            config['password'] = custom_password
        
        # Encode password สำหรับ URL
        encoded_password = quote_plus(config['password'])
        
        return f"postgresql://{config['username']}:{encoded_password}@{config['host']}:{config['port']}/{config['database']}"
    
    def generate_all_urls(self):
        """สร้าง URLs ทั้งหมด"""
        urls = {}
        for config_name in self.configs:
            urls[config_name] = self.generate_url(config_name)
        return urls
    
    def generate_connection_info(self):
        """สร้างข้อมูลการเชื่อมต่อแบบละเอียด"""
        info = {
            "thai_lunar_calendar_connections": {
                "local_database": {
                    "description": "Local PostgreSQL Database",
                    "url": self.generate_url('local'),
                    "web_interface": "https://www.postgresql.org/download/windows/",
                    "pgadmin_url": "http://localhost/pgadmin4",
                    "config": self.configs['local']
                },
                "remote_database": {
                    "description": "Remote PostgreSQL Database", 
                    "url": self.generate_url('remote'),
                    "config": self.configs['remote']
                },
                "server_port": {
                    "description": "Thai Lunar Server on Port 5433",
                    "url": self.generate_url('server'),
                    "server_endpoint": "http://localhost:5433",
                    "telnet_command": "telnet localhost 5433",
                    "config": self.configs['server']
                }
            },
            "usage_examples": {
                "python_psycopg2": {
                    "code": "import psycopg2\nconn = psycopg2.connect('{}')".format(self.generate_url('local')),
                    "description": "Python psycopg2 connection"
                },
                "python_sqlalchemy": {
                    "code": "from sqlalchemy import create_engine\nengine = create_engine('{}')".format(self.generate_url('local')),
                    "description": "Python SQLAlchemy connection"
                },
                "nodejs": {
                    "code": "const { Pool } = require('pg');\nconst pool = new Pool({ connectionString: '{}' });".format(self.generate_url('local')),
                    "description": "Node.js pg connection"
                },
                "command_line": {
                    "code": "psql '{}'".format(self.generate_url('local')),
                    "description": "Command line psql connection"
                }
            },
            "web_resources": [
                "https://www.postgresql.org/download/windows/",
                "https://www.pgadmin.org/download/",
                "https://dbeaver.io/download/",
                "https://www.postgresql.org/docs/"
            ]
        }
        return info

def main():
    """ฟังก์ชันหลัก"""
    print("🔗 Thai Lunar Calendar - Connection URL Generator")
    print("=" * 60)
    
    generator = ConnectionURLGenerator()
    
    # สร้าง URLs ทั้งหมด
    print("\n📡 Connection URLs:")
    print("-" * 30)
    urls = generator.generate_all_urls()
    
    for name, url in urls.items():
        print(f"\n{name.upper()}:")
        print(f"  {url}")
    
    # สร้างข้อมูลแบบละเอียด
    print("\n" + "=" * 60)
    print("📋 Complete Connection Information:")
    print("-" * 30)
    
    info = generator.generate_connection_info()
    print(json.dumps(info, indent=2, ensure_ascii=False))
    
    # เขียนไฟล์ JSON
    with open('connection_info.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    
    print("\n💾 Connection info saved to 'connection_info.json'")
    
    # คำแนะนำการใช้งาน
    print("\n" + "=" * 60)
    print("💡 Usage Tips:")
    print("-" * 30)
    print("1. Update passwords in the URLs before using")
    print("2. Test local database first: postgresql://thaiHub:password@localhost:5432/thai-hub-local")
    print("3. Use pgAdmin4 for database management")
    print("4. Server endpoint: http://localhost:5433")
    print("5. Download PostgreSQL: https://www.postgresql.org/download/windows/")

if __name__ == "__main__":
    main()