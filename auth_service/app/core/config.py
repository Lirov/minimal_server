import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "auth_service"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./auth.db")  # default for local dev

settings = Settings()
