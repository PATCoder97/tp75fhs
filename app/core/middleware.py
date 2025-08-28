# app/core/middleware.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        ms = (time.time() - start) * 1000
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} [{ms:.2f}ms]")
        return response

def init_middleware(app: FastAPI):
    # Setup logging
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
        force=True
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # PROD nên chỉ định domain cụ thể
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Logging
    app.add_middleware(LoggingMiddleware)
