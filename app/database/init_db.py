# app/database/init_db.py
from app.database.session import engine, AsyncSessionLocal
from app.database.base import Base
from app.database.seed import seed_initial_data

async def create_tables() -> None:
    import app.models  # đảm bảo đã load models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_data_async(session) -> None:
    # ví dụ seed; bỏ qua nếu chưa cần
    pass

async def init_db(seed: bool = False) -> None:
    # Import all models
    from app.models.user import User
    from app.models.performance import Performance
    from app.models.dorm_utility import DormUtility
    
    await create_tables()
    # Seed initial data
    async with AsyncSessionLocal() as session:
        await seed_initial_data(session)
