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

def get_database_config():
    """Get database configuration from environment variables"""
    required_vars = ['DB_USERNAME', 'DB_PASSWORD']
    for var in required_vars:
        if not os.getenv(var):
            print(f"Error: {var} not found in .env file!")
            sys.exit(1)

    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME', 'mcp_brandwatch')
    }

def create_database():
    """Create database if it doesn't exist"""
    try:
        # Load environment variables
        load_env()
        
        # Get database configuration
        db_config = get_database_config()
        
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