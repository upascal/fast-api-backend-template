# FastAPI Database Template

A clean, production-ready FastAPI template with database integration, authentication, and user management. Based on Fast API Best Practices by [Zhanymkanov](https://github.com/zhanymkanov/fastapi-best-practices)
## Features

- FastAPI setup with CORS middleware
- PostgreSQL database integration
- SQLAlchemy ORM with async support
- Alembic for database migrations
- JWT authentication
- User management system
- Environment configuration
- Docker support

## Project Structure

```
├── alembic/            # Database migrations
├── src/
│   ├── auth/          # Authentication
│   ├── core/          # Core functionality
│   ├── db/            # Database
│   └── users/         # User management
├── tests/             # Test files
├── .env.example       # Environment variables example
├── alembic.ini        # Alembic configuration
├── docker-compose.yml # Docker compose configuration
└── requirements.txt   # Python dependencies
```

## Getting Started

### Prerequisites
- Docker Desktop installed
- PostgreSQL client (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/upascal/fast-api-db-template.git
cd fast-api-db-template
```

2. Configure environment variables:
```bash
cp .env.example .env
```
Edit `.env` file with your credentials:
```ini
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/fastapi_db
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/fastapi_db

# Authentication
JWT_SECRET=your-secure-key-here
JWT_ALGORITHM=HS256
```

3. Start services:
```bash
docker-compose up -d --build
```

4. Run database migrations:
```bash
docker-compose exec api alembic upgrade head
```

5. Verify services are running:
```bash
docker-compose ps
```

### Accessing the API
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/api/v1/health`

### Example Request
Create a new user:
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

## Key Configuration

| Environment Variable         | Description                          | Default                              |
|------------------------------|--------------------------------------|--------------------------------------|
| `DATABASE_URL`               | PostgreSQL connection URL            | postgresql+asyncpg://postgres:postgres@db:5432/fastapi_db |
| `JWT_SECRET`                 | Secret key for JWT tokens            | (required - set in .env)             |
| `JWT_ALGORITHM`              | Algorithm for JWT tokens             | HS256                                |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| Token expiration time                | 30                                   |
| `CORS_ORIGINS`               | Allowed origins for CORS             | ["http://localhost:3000"]            |

## API Documentation

Access these endpoints once the service is running:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/api/v1/health`
