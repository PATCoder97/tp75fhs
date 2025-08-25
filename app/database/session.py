# app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from app.core.config import settings

# Lấy DATABASE_URL từ cấu hình
DATABASE_URL = settings.DATABASE_URL

# Engine (sync)
engine = create_engine(
    DATABASE_URL,
    echo=False,           # bật True để debug SQL
    pool_pre_ping=True,   # tự check connection trước khi dùng
    future=True
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True
)

# Dependency dùng trong FastAPI route
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
