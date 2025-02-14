from unittest.mock import patch
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app

@pytest.fixture
async def client():
    """Fixture to create a FastAPI test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost"
    ) as client:
        yield client


@patch("src.auth.service.login")
async def test_login(mock_login, mock_db, client):
    """Test login endpoint."""
    mock_token = {"access_token": "test_token", "token_type": "bearer"}
    mock_login.return_value = mock_token

    response = await client.post(
        "/api/v1/auth/token",
        data={"username": "test@example.com", "password": "password123"}
    )

    assert response.status_code == 200
    assert response.json() == mock_token


@patch("src.auth.dependencies.get_current_user")
async def test_read_users_me(mock_get_current_user, mock_user, client):
    """Test get current user endpoint."""
    mock_get_current_user.return_value = mock_user

    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": mock_user
    }


@patch("src.auth.dependencies.get_current_user")
async def test_read_users_me_unauthorized(mock_get_current_user, client):
    """Test get current user endpoint with no token."""
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
