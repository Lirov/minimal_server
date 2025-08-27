from fastapi import FastAPI
from app.routes.auth import router as auth_router

app = FastAPI(title="Auth Service", version="0.1.0")
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
