"""
Конфигурация базы данных PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL из переменных окружения
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/vendhub"
)

# Создание engine с пулом соединений
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    echo=False  # Логирование SQL запросов (для дебага)
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base для моделей
Base = declarative_base()


def get_db():
    """
    Dependency для получения database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Инициализация базы данных (создание таблиц)
    """
    Base.metadata.create_all(bind=engine)
