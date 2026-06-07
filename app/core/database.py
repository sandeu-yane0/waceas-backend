from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

def _build_url(url: str) -> str:
    # Convertit postgresql:// → postgresql+psycopg:// pour psycopg v3
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    return url

_is_sqlite = "sqlite" in settings.DATABASE_URL
_db_url = settings.DATABASE_URL if _is_sqlite else _build_url(settings.DATABASE_URL)

engine = create_engine(
    _db_url,
    connect_args={"check_same_thread": False} if _is_sqlite else {},
    pool_pre_ping=True,
    pool_timeout=20,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
