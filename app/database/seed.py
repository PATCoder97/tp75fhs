from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import get_password_hash

async def seed_initial_data(db: AsyncSession) -> None:
    # Create admin user if not exists
    admin_user = await db.get(User, "VNW0014732")
    if not admin_user:
        admin = User(
            user_id="VNW0014732",
            password_hash=get_password_hash("123456"),
            full_name="Tuấn",
            role="admin",
            is_active=True
        )
        db.add(admin)
        await db.commit()
