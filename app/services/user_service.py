from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate) -> User:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            user_id=user.user_id,
            password_hash=hashed_password,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: str, user: UserUpdate) -> Optional[User]:
        db_user = self.get_user(user_id)
        if not db_user:
            return None
        
        update_data = user.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = pwd_context.hash(update_data.pop("password"))
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: str) -> bool:
        db_user = self.get_user(user_id)
        if not db_user:
            return False
        self.db.delete(db_user)
        self.db.commit()
        return True
