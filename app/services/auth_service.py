from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from app.services.user_service import UserService

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def authenticate(self, user_id: str, password: str) -> Optional[dict]:
        user = self.user_service.get_user(user_id)
        if not user or not verify_password(password, user.password_hash):
            return None
            
        access_token = create_access_token(data={"sub": user.user_id})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
