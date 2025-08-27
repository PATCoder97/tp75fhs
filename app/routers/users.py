from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user_service import UserService
from app.core.security import admin_required, admin_or_mod_required

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, dependencies=[Depends(admin_required)])
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    existing_user = await service.get_user(user.user_id)
    if existing_user:
        raise HTTPException(status_code=409, detail=f"User {user.user_id} already exists")
    return await service.create_user(user)

@router.get("/", response_model=List[UserOut], dependencies=[Depends(admin_required)])
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.get_users(skip, limit)

@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(admin_required)])
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut, dependencies=[Depends(admin_required)])
async def update_user(user_id: str, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    updated_user = await service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", dependencies=[Depends(admin_required)])
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    if not await service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
