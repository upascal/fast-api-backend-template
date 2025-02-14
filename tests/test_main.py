from httpx import AsyncClient, ASGITransport
from src.main import app
import pytest

@pytest.fixture
async def client():
    """Fixture to create a FastAPI test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client


async def test_health_check(client):
    """Test the health check endpoint."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "version": "1.0.0"
    }


async def test_cors_middleware(client):
    """Test that CORS middleware is properly configured."""
    # Test with allowed origin
    response = await client.get(
        "/api/v1/health",
        headers={"Origin": "http://localhost:3000"}
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "access-control-allow-credentials" in response.headers
    assert response.headers["access-control-allow-credentials"] == "true"
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers

    # Test with disallowed origin
    response = await client.get(
        "/api/v1/health",
        headers={"Origin": "http://invalid-origin.com"}
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers
