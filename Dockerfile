FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Không set CMD cố định ở đây; sẽ override bằng docker-compose
# CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
