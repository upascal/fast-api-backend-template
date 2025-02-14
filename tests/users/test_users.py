from unittest.mock import patch
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def client():
    """Fixture to create a FastAPI test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client


@patch("src.users.service.create")
async def test_create_user(mock_create, mock_db, client):
    """Test create user endpoint."""
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    mock_create.return_value = {
        **user_data,
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "is_active": True,
        "is_superuser": False,
        "created_at": "2025-02-14T20:00:00",
        "updated_at": "2025-02-14T20:00:00"
    }

    response = await client.post("/api/v1/users", json=user_data)

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["message"] == "User created successfully"
    assert "data" in response.json()


@patch("src.auth.dependencies.get_current_active_superuser")
@patch("src.users.service.get_multi")
async def test_get_users(mock_get_multi, mock_superuser, mock_db, client):
    """Test get all users endpoint."""
    mock_users = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "user1@example.com",
            "is_active": True,
            "is_superuser": False,
            "created_at": "2025-02-14T20:00:00",
            "updated_at": "2025-02-14T20:00:00"
        },
        {
            "id": "456e4567-e89b-12d3-a456-426614174000",
            "email": "user2@example.com",
            "is_active": True,
            "is_superuser": False,
            "created_at": "2025-02-14T20:00:00",
            "updated_at": "2025-02-14T20:00:00"
        }
    ]
    mock_get_multi.return_value = mock_users
    mock_superuser.return_value = True

    response = await client.get(
        "/api/v1/users",
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(response.json()["data"]) == 2


@patch("src.auth.dependencies.get_current_user")
@patch("src.users.service.get_by_id")
async def test_get_user(mock_get_by_id, mock_get_current_user, mock_user, mock_db, client):
    """Test get user by ID endpoint."""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_get_by_id.return_value = mock_user
    mock_get_current_user.return_value = mock_user

    response = await client.get(
        f"/api/v1/users/{user_id}",
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"] == mock_user


@patch("src.auth.dependencies.get_current_user")
@patch("src.users.service.update")
async def test_update_user(mock_update, mock_get_current_user, mock_user, mock_db, client):
    """Test update user endpoint."""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    update_data = {"full_name": "Updated Name"}
    updated_user = {**mock_user, "full_name": "Updated Name"}
    mock_update.return_value = updated_user
    mock_get_current_user.return_value = mock_user

    response = await client.put(
        f"/api/v1/users/{user_id}",
        json=update_data,
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "User updated successfully"
    assert response.json()["data"] == updated_user


@patch("src.auth.dependencies.get_current_user")
@patch("src.users.service.delete")
async def test_delete_user(mock_delete, mock_get_current_user, mock_user, mock_db, client):
    """Test delete user endpoint."""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_get_current_user.return_value = mock_user
    mock_delete.return_value = None

    response = await client.delete(
        f"/api/v1/users/{user_id}",
    )

    assert response.status_code == 204
