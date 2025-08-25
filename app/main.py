# app/main.py
from fastapi import FastAPI
from app.database.init_db import init_db
from app.routers import users

app = FastAPI(title="TP75 FHS")

# Đăng ký routers:
app.include_router(users.router)

# # (Tuỳ chọn) Khởi tạo DB khi start app trong môi trường DEV/DEMO
# @app.on_event("startup")
# def on_startup():
#     init_db()
