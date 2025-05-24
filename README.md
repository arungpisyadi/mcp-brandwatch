# MCP Brandwatch API

A FastAPI-based implementation of the Brandwatch API using the Model-Content-Protocol (MCP) pattern.

## Overview

This project implements a RESTful API for interacting with the Brandwatch Consumer Research platform. It follows the MCP (Model-Content-Protocol) pattern for clean architecture and separation of concerns.

## Requirements

- Python 3.8+
- MySQL 8.0+
- Virtual Environment (recommended)
- Docker and Docker Compose (for containerized deployment)

## Features

- Authentication using OAuth2
- Rate limiting (30 calls per 10 minutes)
- Comprehensive error handling
- Async operations
- Data validation using Pydantic
- Logging
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
│   │   ├── mcp_models.py
│   │   ├── brandwatch_protocol.py
│   │   └── security.py
│   ├── consumers/
│   │   └── brandwatch_consumer.py
│   ├── routers/
│   │   └── brandwatch.py
│   ├── database.py
│   └── main.py
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Authentication

All endpoints require OAuth2 authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### User Endpoints

#### Get Current User
```http
GET /brandwatch/me
```
Returns the current user's details.

#### Update Current User
```http
PUT /brandwatch/me
```
Update current user's details.

Request Body:
```json
{
    "email": "user@example.com",
    "username": "username",
    "full_name": "Full Name",
    "role": "user",
    "is_active": true
}
```

### User Management Endpoints

#### Create User
```http
POST /brandwatch/users
```
Create a new user.

Request Body:
```json
{
    "email": "user@example.com",
    "username": "username",
    "full_name": "Full Name",
    "role": "user",
    "is_active": true
}
```

#### Get User
```http
GET /brandwatch/users/{user_id}
```
Get user details by ID.

#### Update User
```http
PUT /brandwatch/users/{user_id}
```
Update user details.

Request Body:
```json
{
    "email": "user@example.com",
    "username": "username",
    "full_name": "Full Name",
    "role": "user",
    "is_active": true
}
```

#### Delete User
```http
DELETE /brandwatch/users/{user_id}
```
Delete a user.

### Client Endpoints

#### Create Client
```http
POST /brandwatch/clients
```
Create a new client.

Request Body:
```json
{
    "name": "Client Name",
    "description": "Client Description",
    "api_key": "api-key",
    "rate_limit": 30,
    "is_active": true
}
```

#### Get Client
```http
GET /brandwatch/clients/{client_id}
```
Get client details by ID.

#### Update Client
```http
PUT /brandwatch/clients/{client_id}
```
Update client details.

Request Body:
```json
{
    "name": "Client Name",
    "description": "Client Description",
    "api_key": "api-key",
    "rate_limit": 30,
    "is_active": true
}
```

#### Delete Client
```http
DELETE /brandwatch/clients/{client_id}
```
Delete a client.

### Query Endpoints

#### Create Query
```http
POST /brandwatch/queries
```
Create a new query.

Request Body:
```json
{
    "name": "Query Name",
    "boolean_query": "query string",
    "languages": ["en"],
    "content_sources": ["twitter", "blog", "forum"],
    "start_date": "2024-01-01",
    "location_filter": {
        "included": ["USA"],
        "excluded": []
    },
    "image_filter": {
        "type": "all"
    }
}
```

#### Validate Query
```http
POST /brandwatch/queries/validate
```
Validate a query before creation.

Request Body: Same as Create Query

### Mention Endpoints

#### Get Mentions
```http
GET /brandwatch/mentions
```
Get mentions for a specific query.

Query Parameters:
```json
{
    "query_id": "query-id",
    "start_date": "2024-01-01",
    "end_date": "2024-03-20",
    "page_size": 100,
    "page": 0,
    "order_by": "added",
    "order_direction": "desc"
}
```

### Project Endpoints

#### Create Project
```http
POST /brandwatch/projects
```
Create a new project.

Request Body:
```json
{
    "name": "Project Name",
    "description": "Project Description"
}
```

#### Get Projects
```http
GET /brandwatch/projects
```
Get all projects.

## Environment Variables

Create a `.env` file with the following variables:

```env
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

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mcp-brandwatch.git
cd mcp-brandwatch
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. Create MySQL database:
```sql
CREATE DATABASE mcp_brandwatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. Run database migrations:
```bash
alembic upgrade head
```

7. Run the application:
```bash
uvicorn app.main:app --reload
```

### Docker Deployment

1. Build and start the containers:
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

## API Documentation

After running the application, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Rate Limiting

The API implements rate limiting according to Brandwatch's specifications:
- 30 calls per 10 minutes per client
- Rate limits are applied at the client level, not the user level

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
