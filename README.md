# FastAPI Database Template

A clean, production-ready FastAPI template with database integration, authentication, and user management. Based on Fast API Best Practices by [Tomasz Chowaniec](https://github.com/tomaszchow/fastapi-best-practices).

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

1. Clone this template:
```bash
git clone https://github.com/upascal/fast-api-db-template.git
cd fast-api-db-template
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

4. Copy `.env.example` to `.env` and update the variables:
```bash
cp .env.example .env
```

5. Start the database:
```bash
docker-compose up -d
```

6. Run migrations:
```bash
alembic upgrade head
```

7. Start the application:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation at `http://localhost:8000/docs`
- ReDoc documentation at `http://localhost:8000/redoc`
