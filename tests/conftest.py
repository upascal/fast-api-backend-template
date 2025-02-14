import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient
from fastapi import FastAPI
from src.main import app as fastapi_app


@pytest.fixture
def mock_db():
    """Fixture for mocking the database session."""
    return AsyncMock()


@pytest.fixture
def mock_user():
    """Fixture for a regular user."""
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False,
        "full_name": "Test User"
    }


@pytest.fixture
def mock_superuser():
    """Fixture for a superuser."""
    return {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "email": "admin@example.com",
        "is_active": True,
        "is_superuser": True,
        "full_name": "Admin User"
    }


from datetime import datetime, timedelta
from jose import jwt
from src.core.config import settings

@pytest.fixture
def mock_token(mock_user):
    """Fixture for generating a valid JWT token."""
    token_data = {
        "user_id": mock_user["id"],
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    return {
        "access_token": jwt.encode(
            token_data,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        ),
        "token_type": "bearer"
    }


@pytest.fixture
async def client(mock_token):
    """Fixture for creating an async test client with authentication support."""
    async with AsyncClient(
        app=fastapi_app,
        base_url="http://test",
        headers={"Authorization": f"Bearer {mock_token['access_token']}"}
    ) as ac:
        yield ac
