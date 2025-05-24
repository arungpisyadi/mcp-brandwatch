#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

def load_env():
    """Load environment variables from .env file"""
    env_path = Path('.') / '.env'
    if not env_path.exists():
        print("Error: .env file not found!")
        sys.exit(1)
    load_dotenv(env_path)

def parse_database_url():
    """Parse DATABASE_URL from environment variables"""
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found in .env file!")
        sys.exit(1)

    # Format: mysql://username:password@host:port/database
    try:
        # Remove mysql:// prefix
        db_url = db_url.replace('mysql://', '')
        
        # Split into parts
        auth, rest = db_url.split('@')
        username, password = auth.split(':')
        host_port, database = rest.split('/')
        
        # Handle port if specified
        if ':' in host_port:
            host, port = host_port.split(':')
            port = int(port)
        else:
            host = host_port
            port = 3306

        return {
            'host': host,
            'port': port,
            'user': username,
            'password': password,
            'database': database
        }
    except Exception as e:
        print(f"Error parsing DATABASE_URL: {e}")
        sys.exit(1)

def create_database():
    """Create database if it doesn't exist"""
    try:
        # Load environment variables
        load_env()
        
        # Parse database configuration
        db_config = parse_database_url()
        
        # Connect to MySQL server without database
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{db_config['database']}' created successfully or already exists")
            
            # Test connection to the new database
            cursor.execute(f"USE {db_config['database']}")
            print(f"Successfully connected to database '{db_config['database']}'")
            
            cursor.close()
            connection.close()
            print("MySQL connection closed")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_database() 