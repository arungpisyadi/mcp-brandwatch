#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if required Python packages are installed
if ! python3 -c "import mysql.connector" &> /dev/null; then
    echo "Installing required Python packages..."
    pip3 install mysql-connector-python python-dotenv
fi

# Run the Python script
echo "Creating database..."
python3 scripts/create_db.py

# Check if the script executed successfully
if [ $? -eq 0 ]; then
    echo "Database setup completed successfully"
else
    echo "Error: Database setup failed"
    exit 1
fi 