from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: str) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.user_id == user_id.upper()))
        return result.scalar_one_or_none()

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create_user(self, user: UserCreate) -> User:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            user_id=user.user_id.upper(),
            password_hash=hashed_password,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_user(self, user_id: str, user: UserUpdate) -> Optional[User]:
        db_user = await self.get_user(user_id)
        if not db_user:
            return None
        
        update_data = user.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = pwd_context.hash(update_data.pop("password"))
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: str) -> bool:
        db_user = await self.get_user(user_id)
        if not db_user:
            return False
        await self.db.delete(db_user)
        await self.db.commit()
        return True
