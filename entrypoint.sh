#!/bin/bash

# Check if required Python packages are installed
if ! python3 -c "import mysql.connector" &> /dev/null; then
    echo "Installing required Python packages..."
    pip3 install mysql-connector-python python-dotenv
fi

# Run the database creation script
echo "Creating database..."
python3 scripts/create_db.py

# Check if the script executed successfully
if [ $? -eq 0 ]; then
    echo "Database setup completed successfully"
else
    echo "Error: Database setup failed"
    exit 1
fi

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} 