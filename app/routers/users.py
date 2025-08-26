from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user_service import UserService
from app.core.security import admin_required, admin_or_mod_required

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, dependencies=[Depends(admin_required)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    existing_user = service.get_user(user.user_id)
    if existing_user:
        raise HTTPException(status_code=409, detail=f"User {user.user_id} already exists")
    return service.create_user(user)

@router.get("/", response_model=List[UserOut], dependencies=[Depends(admin_required)])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_users(skip, limit)

@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(admin_or_mod_required)])
def get_user(user_id: str, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut, dependencies=[Depends(admin_or_mod_required)])
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    updated_user = service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", dependencies=[Depends(admin_or_mod_required)])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    service = UserService(db)
    if not service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
