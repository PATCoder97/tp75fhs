# app/main.py
from fastapi import FastAPI
from app.database.init_db import init_db
from app.routers import users, auth, fhshrs, performance, dorm_utility
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
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(fhshrs.router, prefix="/api")
app.include_router(performance.router, prefix="/api")
app.include_router(dorm_utility.router, prefix="/api")


# Enable auto DB initialization on startup
@app.on_event("startup")
async def on_startup():
    await init_db()
