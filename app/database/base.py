# app/database/base.py
from sqlalchemy.orm import DeclarativeBase

# Base dùng để tất cả models kế thừa
class Base(DeclarativeBase):
    pass

# IMPORT MODELS VÀO ĐÂY để Alembic/metadata thấy hết (tránh circular)
# from app.models.user import User
# from app.models.product import Product
