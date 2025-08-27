FROM python:3.11-slim

WORKDIR /app

# Cài toolchain để pip compile các package không có wheel sẵn (bcrypt, cffi, cryptography, ...)
# Giữ layer riêng để có thể remove sau khi cài xong dependencies (giảm size)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    cargo \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Không set CMD cố định ở đây; sẽ override bằng docker-compose
# CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
