# app/database/init_db.py
from sqlalchemy.orm import Session
from app.database.session import engine, SessionLocal
from app.database.base import Base
# from app.models.user import User  # nếu cần seed
# from app.schemas.user import UserCreate  # nếu bạn muốn truyền schema

def create_tables() -> None:
    """
    Tạo toàn bộ bảng theo models đã khai báo (Base.metadata).
    Chạy 1 lần khi khởi tạo hệ thống (hoặc dùng Alembic migration ở prod).
    """
    Base.metadata.create_all(bind=engine)

def seed_data(db: Session) -> None:
    """
    Thêm dữ liệu ban đầu (admin user, roles, master data...).
    Tránh seed trùng bằng cách kiểm tra đã tồn tại chưa.
    """
    # Ví dụ minh họa (giả sử có model User):
    # if not db.query(User).filter(User.email == "admin@example.com").first():
    #     admin = User(email="admin@example.com", hashed_password=hash_pw("changeme"))
    #     db.add(admin)
    #     db.commit()
    #     db.refresh(admin)
    pass

def init_db() -> None:
    """
    Gọi khi app start (tuỳ chọn) hoặc tạo 1 lệnh riêng.
    """
    create_tables()
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
