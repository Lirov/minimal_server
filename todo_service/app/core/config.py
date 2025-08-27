import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "todo_service"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

settings = Settings()
