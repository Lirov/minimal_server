import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta

from main import app
from app.services.user_service import UserService

client = TestClient(app)

@pytest.fixture
def user_service():
    """Fresh user service for each test."""
    return UserService()

@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

class TestUserRegistration:
    def test_register_user_success(self, test_user_data):
        """Test successful user registration."""
        response = client.post("/auth/register", json=test_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "password" not in data  # Password should not be returned

    def test_register_user_duplicate_email(self, test_user_data):
        """Test registration with existing email."""
        # Register first user
        client.post("/auth/register", json=test_user_data)
        
        # Try to register with same email
        response = client.post("/auth/register", json=test_user_data)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_register_user_invalid_email(self):
        """Test registration with invalid email format."""
        response = client.post("/auth/register", json={
            "email": "invalid-email",
            "password": "testpassword123"
        })
        assert response.status_code == 422

    def test_register_user_short_password(self):
        """Test registration with short password."""
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "123"
        })
        assert response.status_code == 409

class TestUserLogin:
    def test_login_success(self, test_user_data):
        """Test successful login."""
        # Register user first
        client.post("/auth/register", json=test_user_data)
        
        # Login
        response = client.post("/auth/login", json=test_user_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, test_user_data):
        """Test login with wrong password."""
        # Register user first
        client.post("/auth/register", json=test_user_data)
        
        # Try to login with wrong password
        response = client.post("/auth/login", json={
            "email": test_user_data["email"],
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self):
        """Test login with non-existent user."""
        response = client.post("/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        })
        assert response.status_code == 401

class TestJWTToken:
    def test_jwt_token_valid(self, test_user_data):
        """Test that JWT token is valid and contains expected claims."""
        # Use unique email for this test
        unique_user_data = {
            "email": "jwt_test@example.com",
            "password": test_user_data["password"]
        }
        
        # Register and login
        register_response = client.post("/auth/register", json=unique_user_data)
        user_id = register_response.json()["id"]
        response = client.post("/auth/login", json=unique_user_data)
        
        token = response.json()["access_token"]
        
        # Decode token (without verification for testing)
        decoded = jwt.decode(token, options={"verify_signature": False})
        assert decoded["sub"] == user_id
        assert "exp" in decoded
        assert "iat" in decoded

    def test_jwt_token_expiration(self, test_user_data):
        """Test that JWT token has expiration time."""
        # Register and login
        client.post("/auth/register", json=test_user_data)
        response = client.post("/auth/login", json=test_user_data)
        
        token = response.json()["access_token"]
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        # Check that expiration is in the future
        exp_time = datetime.fromtimestamp(decoded["exp"])
        assert exp_time > datetime.now()

class TestUserService:
    def test_create_user(self, user_service):
        """Test user service create_user method."""
        user = user_service.create_user(
            email="test@example.com",
            password="testpassword123"
        )
        assert user["email"] == "test@example.com"
        assert "id" in user
        assert "password_hash" in user
        assert user["password_hash"] != "testpassword123"  # Should be hashed

    def test_create_duplicate_user(self, user_service):
        """Test creating user with existing email."""
        user_service.create_user(
            email="test@example.com",
            password="testpassword123"
        )
        
        with pytest.raises(ValueError, match="User already exists"):
            user_service.create_user(
                email="test@example.com",
                password="anotherpassword"
            )

    def test_authenticate_valid_user(self, user_service):
        """Test authentication with valid credentials."""
        user_service.create_user(
            email="test@example.com",
            password="testpassword123"
        )
        
        user = user_service.authenticate(
            email="test@example.com",
            password="testpassword123"
        )
        assert user is not None
        assert user["email"] == "test@example.com"

    def test_authenticate_invalid_password(self, user_service):
        """Test authentication with wrong password."""
        user_service.create_user(
            email="test@example.com",
            password="testpassword123"
        )
        
        user = user_service.authenticate(
            email="test@example.com",
            password="wrongpassword"
        )
        assert user is None

    def test_authenticate_nonexistent_user(self, user_service):
        """Test authentication with non-existent user."""
        user = user_service.authenticate(
            email="nonexistent@example.com",
            password="testpassword123"
        )
        assert user is None

class TestHealthCheck:
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
