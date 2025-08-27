from app.schemas.auth import UserCreate, UserLogin, UserOut
from app.services.user_service import user_service
from app.core.security import create_access_token
from app.core.config import settings

# register_user()
def register_user(payload: UserCreate) -> UserOut:
    try:
        user = user_service.create_user(email=payload.email, password=payload.password)
    except ValueError as e:
        # Let the route translate into 409/400 as needed
        raise e
    return UserOut(id=user["id"], email=user["email"])

# login_user()
def login_user(payload: UserLogin) -> str | None:
    user = user_service.authenticate(email=payload.email, password=payload.password)
    if not user:
        return None
    token = create_access_token(
        sub=user["id"],
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        secret=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return token
