# app/core/middleware.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        ms = (time.time() - start) * 1000
        # log ngắn gọn: METHOD PATH status time
        print(f"{request.method} {request.url.path} -> {response.status_code} [{ms:.2f}ms]")
        return response

def init_middleware(app: FastAPI):
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
