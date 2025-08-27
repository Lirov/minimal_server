import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta
from main import app

@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def test_todo_data():
    """Sample todo data for testing."""
    return {
        "title": "Test todo item",
        "completed": False
    }

@pytest.fixture
def mock_auth_token():
    """Mock JWT token for testing."""
    payload = {
        "sub": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, "test-secret", algorithm="HS256")

@pytest.fixture
def auth_headers(mock_auth_token):
    """Headers with authentication token."""
    return {"Authorization": f"Bearer {mock_auth_token}"}

@pytest.fixture
def authenticated_client(client, auth_headers):
    """Client with authentication headers."""
    client.headers.update(auth_headers)
    return client
