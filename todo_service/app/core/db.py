from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session
from .config import settings

engine = create_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)

def init_db():
    # For local dev convenience; production relies on Alembic
    SQLModel.metadata.create_all(engine)

@contextmanager
def session_scope():
    with Session(engine) as session:
        yield session
