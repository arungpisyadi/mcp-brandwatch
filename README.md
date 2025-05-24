# MCP Brandwatch API

## Overview
MCP Brandwatch API is a FastAPI application that integrates with the Brandwatch API for social media data management.

## Features
- JWT Authentication
- MySQL Database Integration
- Brandwatch API Integration
- RESTful API Endpoints
- API Documentation with Swagger/ReDoc
- Docker Support
- Rate Limiting
- Comprehensive Error Handling
- Async Operations
- Data Validation using Pydantic
- Logging

## Requirements
- Python 3.8+
- MySQL 8.0+
- Docker (optional)

## Project Structure
```
mcp-brandwatch/
├── app/
│   ├── core/
│   │   ├── brandwatch_protocol.py
│   │   ├── mcp_models.py
│   │   └── config.py
│   ├── consumers/
│   │   └── brandwatch_consumer.py
│   ├── models/
│   │   └── database.py
│   ├── routers/
│   │   └── brandwatch.py
│   ├── database.py
│   └── main.py
├── scripts/
│   ├── create_db.py
│   └── create_db.sh
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
└── requirements.txt
```

## API Endpoints

### Authentication

#### Get Access Token
```http
POST /brandwatch/auth/token
```
Get access token for API authentication.

Request Body:
```json
{
    "username": "your@username.com",
    "password": "yourpassword",
    "grant_type": "api-password",
    "client_id": "brandwatch-api-client"
}
```

Response:
```json
{
    "access_token": "aa000000-0aaa-0000-0a00-aa00a000a00a",
    "token_type": "bearer",
    "expires_in": 31535999,
    "scope": "read trust write"
}
```

Note: The access token is valid for one year by default. Include it in subsequent requests using either:
1. Authorization header: `Authorization: Bearer <access_token>`
2. URL parameter: `?access_token=<access_token>`

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

## Database Configuration

### Local Development
1. Create `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

2. Update database configuration in `.env`:
   ```env
   # For local database
   DATABASE_URL=mysql://root:password@localhost:3306/mcp_brandwatch
   
   # For remote database (RDS)
   DATABASE_URL=mysql://username:password@your-rds-endpoint:3306/mcp_brandwatch
   ```

3. Create database using script:
   ```bash
   # Give execute permission
   chmod +x scripts/create_db.sh
   
   # Run script
   ./scripts/create_db.sh
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

### Docker Deployment
1. Update database configuration in `.env`:
   ```env
   DATABASE_URL=mysql://username:password@your-rds-endpoint:3306/mcp_brandwatch
   ```

2. Run application:
   ```bash
   docker-compose up --build
   ```

### Database Scripts
Scripts `create_db.py` and `create_db.sh` provide functionality to:
- Read database configuration from `.env`
- Create database if it doesn't exist
- Set character set to `utf8mb4` and collation to `utf8mb4_unicode_ci`
- Verify database connection

### Best Practices
1. **Security**:
   - Never commit `.env` file
   - Use strong passwords
   - Restrict database access with firewall
   - Enable SSL for database connections

2. **RDS Configuration**:
   - Use appropriate parameter group
   - Enable automatic backups
   - Monitor database performance
   - Use multi-AZ for high availability
   - Adjust instance type based on needs

3. **Maintenance**:
   - Regular database backups
   - Monitor disk space usage
   - Optimize query performance
   - Regular database updates

## Environment Variables
```env
# Application Configuration
PORT=8000

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
1. Clone repository:
   ```bash
   git clone https://github.com/your-username/mcp-brandwatch.git
   cd mcp-brandwatch
   ```

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

4. Setup database:
   ```bash
   ./scripts/create_db.sh
   alembic upgrade head
   ```

5. Run application:
   ```bash
   uvicorn app.main:app --reload
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

## API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

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

Response format:
```json
{
    "detail": "Error message"
}
```

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
