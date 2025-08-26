# app/main.py
from fastapi import FastAPI
from app.database.init_db import init_db
from app.routers import users, auth
from app.core.middleware import init_middleware

app = FastAPI(
    title="TP75 FHS",
    description="API for TP75 FHS application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Đăng ký middleware
init_middleware(app)

# Đăng ký routers:
app.include_router(auth.router)
app.include_router(users.router)

# # (Tuỳ chọn) Khởi tạo DB khi start app trong môi trường DEV/DEMO
# @app.on_event("startup")
# def on_startup():
#     init_db()
