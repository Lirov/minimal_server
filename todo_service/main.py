from fastapi import FastAPI
from app.routes.todos import router as todos_router

app = FastAPI(title="Todo Service", version="0.1.0")
app.include_router(todos_router, prefix="/todos", tags=["todos"])

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
