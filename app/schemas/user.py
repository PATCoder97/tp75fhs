# app/schemas/user.py
from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field

# Nếu quyền hạn cố định, bạn có thể giới hạn bằng Literal
RoleLiteral = Literal["admin", "user", "manager", "guest"]

class UserBase(BaseModel):
    full_name: str | None = Field(default=None, max_length=100)
    role: str = Field(..., max_length=20)  # hoặc: RoleLiteral
    is_active: bool = True

class UserCreate(UserBase):
    # user_id dùng để login
    user_id: str = Field(..., min_length=10, max_length=10)
    # nhận plain password từ client để hash ở service
    password: str = Field(..., min_length=6, max_length=128)

class UserUpdate(BaseModel):
    # Cho phép cập nhật từng phần
    full_name: str | None = Field(default=None, max_length=100)
    role: str | None = Field(default=None, max_length=20)  # hoặc: RoleLiteral | None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=6, max_length=128)

class UserOut(BaseModel):
    user_id: str
    full_name: str | None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
