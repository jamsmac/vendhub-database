# Multi-stage build для оптимизации размера
FROM python:3.11-slim as builder

WORKDIR /app

# Установка зависимостей для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Установка только runtime зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование установленных пакетов из builder
COPY --from=builder /root/.local /root/.local

# Добавление в PATH
ENV PATH=/root/.local/bin:$PATH

# Копирование приложения
COPY . .

# Создание директории для логов
RUN mkdir -p logs

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Exposing port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Запуск приложения
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
