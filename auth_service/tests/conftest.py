import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

@pytest.fixture
def registered_user(client, test_user_data):
    """Register a user and return the user data."""
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def auth_token(client, registered_user, test_user_data):
    """Get authentication token for a registered user."""
    response = client.post("/auth/login", json=test_user_data)
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    """Headers with authentication token."""
    return {"Authorization": f"Bearer {auth_token}"}
