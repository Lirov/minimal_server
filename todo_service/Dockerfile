FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY main.py ./
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

EXPOSE 8002
CMD ["alembic", "upgrade", "head", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
