# app/database/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from app.core.config import settings

# Convert DATABASE_URL to async format (postgresql:// -> postgresql+asyncpg://)
ASYNC_DATABASE_URL = settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')

# Async engine
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    future=True
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Async dependency
async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

