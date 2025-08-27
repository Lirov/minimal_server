from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserCreate, UserLogin, Token, UserOut
from app.controllers.auth_controller import register_user, login_user

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate):
    try:
        return register_user(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/login", response_model=Token)
def login(payload: UserLogin):
    token = login_user(payload)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
