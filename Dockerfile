FROM python:3.11-slim

WORKDIR /app

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Force logs to stdout without buffering
CMD ["bash", "-c", "python -u -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info"]
