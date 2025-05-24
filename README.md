# MCP Brandwatch API

API for MCP integration with Brandwatch using FastAPI.

## Requirements

- Python 3.8+
- MySQL 8.0+
- Virtual Environment (recommended)
- Docker and Docker Compose (for containerized deployment)

## Installation

### Local Development

1. Clone this repository
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file and fill in the required configuration:
```
# Database Configuration
DATABASE_URL=mysql://root:password@localhost:3306/mcp_brandwatch

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Brandwatch API Configuration
BRANDWATCH_API_URL=https://api.brandwatch.com
BRANDWATCH_CLIENT_ID=brandwatch-api-client
```

5. Create MySQL database:
```sql
CREATE DATABASE mcp_brandwatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. Run database migrations:
```bash
alembic upgrade head
```

### Docker Deployment
1. Build and run containers:
   ```bash
   docker-compose up --build
   ```

2. The application will be available at http://localhost:8000

3. To stop the containers:
   ```bash
   docker-compose down
   ```

4. To stop the containers and remove volumes:
   ```bash
   docker-compose down -v
   ```

## Running the Application

### Local Development
```bash
uvicorn app.main:app --reload
```

### Docker
```bash
docker-compose up
```

The application will run at http://localhost:8000

## API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Features

- JWT Authentication
- MySQL Database Integration
- Brandwatch API Integration
- RESTful API Endpoints
- API Documentation with Swagger/ReDoc
- Docker Support

## Project Structure

```
mcp-brandwatch/
├── app/
│   ├── core/
│   │   └── security.py
│   ├── models/
│   │   └── user.py
│   ├── routers/
│   │   └── auth.py
│   ├── database.py
│   └── main.py
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

Response format:
```json
{
    "detail": "Error message"
}
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
