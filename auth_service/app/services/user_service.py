import uuid
from typing import Optional
from app.core.security import hash_password, verify_password

class UserService:
    """Minimal in-memory user service for demo/interview purposes."""
    def __init__(self) -> None:
        self._users_by_email: dict[str, dict] = {}

    # create_user()
    def create_user(self, *, email: str, password: str) -> dict:
        if email in self._users_by_email:
            raise ValueError("User already exists")
        user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password_hash": hash_password(password),
        }
        self._users_by_email[email] = user
        return user

    # authenticate()
    def authenticate(self, *, email: str, password: str) -> Optional[dict]:
        user = self._users_by_email.get(email)
        if not user:
            return None
        if not verify_password(password, user["password_hash"]):
            return None
        return user

user_service = UserService()
