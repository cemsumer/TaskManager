FROM python:3.11-slim

WORKDIR /app

# Sisteme gerekli C kütüphanelerini kur (psycopg için zorunlu)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Uygulama ve requirements dosyasını kopyala
COPY ./app /app/app
COPY ./app/requirements.txt /app/requirements.txt

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ortam değişkenlerini tanımla
ENV PROJECT_NAME="Task Manager"
ENV POSTGRES_SERVER="localhost"
ENV POSTGRES_USER="postgres"
ENV FIRST_SUPERUSER="admin@example.com"
ENV FIRST_SUPERUSER_PASSWORD="changeme"

# Uygulamayı başlat
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

