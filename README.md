# Minimal Python Microservices Template (FastAPI + JWT)

Two tiny services, cleanly split into **routes → controllers → services**, with JWT auth:

- **auth_service** (port 8001): register & log in; issues JWTs
- **todo_service** (port 8002): protected CRUD-like endpoints for todos

Uses FastAPI, Pydantic v2, PyJWT, and in-memory stores to keep it interview-friendly and easy to extend.

---

## Quickstart (Docker)

```bash
# From repo root
cp .env.example .env   # optional
docker compose up --build
```

- Auth docs: http://localhost:8001/docs
- Todo docs: http://localhost:8002/docs

## Quickstart (Local Python)

```bash
# Auth service
cd auth_service
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export SECRET_KEY="dev-secret"  # Windows: set SECRET_KEY=dev-secret
uvicorn main:app --reload --port 8001

# Todo service (new terminal)
cd ../todo_service
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="dev-secret"
uvicorn main:app --reload --port 8002
```

## Test Flow

```bash
# 1) Register
curl -X POST http://localhost:8001/auth/register -H "Content-Type: application/json"       -d '{ "email": "me@example.com", "password": "s3cret!" }'

# 2) Login → get token
TOKEN=$(curl -s -X POST http://localhost:8001/auth/login -H "Content-Type: application/json"       -d '{ "email": "me@example.com", "password": "s3cret!" }' | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 3) Use token with Todo service
curl -H "Authorization: Bearer $TOKEN" http://localhost:8002/todos/

# 4) Create a todo
curl -X POST http://localhost:8002/todos/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"       -d '{ "title": "prep interview", "completed": false }'
```

## Structure (per service)

```text
app/
  core/           # config, security (auth_service only)
  routes/         # FastAPI routers
  controllers/    # Orchestrate business actions; pure Python
  services/       # State & integrations (DBs, caches, etc.); in-memory for now
  schemas/        # Pydantic models
main.py           # FastAPI app bootstrap
Dockerfile
requirements.txt
```

## JWT Details

- Token payload: `{ sub: <user_id>, iat, exp }`
- Algo: HS256 (shared secret via `SECRET_KEY` env var in both services)
- Todo service trusts tokens signed by the same `SECRET_KEY`.

## Extending for Interviews

Suggested quick wins to show off:
- Replace in-memory stores with Postgres (SQLModel / SQLAlchemy) + migrations
- Add unit tests (pytest) for controllers & services
- Introduce a gateway (FastAPI + httpx) or Traefik for routing
- Add refresh tokens & role-based authorization
- Add CI (GitHub Actions) and pre-commit hooks
```
