# app/database/init_db.py
from app.database.session import engine
from app.database.base import Base

async def create_tables() -> None:
    import app.models  # đảm bảo đã load models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_data_async(session) -> None:
    # ví dụ seed; bỏ qua nếu chưa cần
    pass

async def init_db(seed: bool = False) -> None:
    await create_tables()
    if seed:
        from app.database.session import AsyncSessionLocal  # async session
        async with AsyncSessionLocal() as db:
            await seed_data_async(db)
