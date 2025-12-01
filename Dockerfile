FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY backend/ ./backend/

# Создание директории для логов
RUN mkdir -p backend/logs

# Порт
EXPOSE 8000

# Запуск
CMD ["sh", "-c", "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
