"""
SQLAlchemy модели для VendHub Database
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date, Index, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    files = relationship("File", back_populates="user", cascade="all, delete-orphan")


class File(Base):
    """Модель загруженного файла"""
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_url = Column(Text, nullable=True)  # S3 URL или путь
    row_count = Column(Integer, default=0)
    headers = Column(JSON, nullable=True)  # Заголовки колонок
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="files")
    records = relationship("Record", back_populates="file", cascade="all, delete-orphan")

    # Индексы
    __table_args__ = (
        Index('idx_files_user_uploaded', 'user_id', 'uploaded_at'),
    )


class Record(Base):
    """Модель записи из Excel файла"""
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"), nullable=False, index=True)
    data = Column(JSON, nullable=False)  # Данные строки в JSON формате
    date_field = Column(Date, nullable=True, index=True)  # Извлеченная дата
    period = Column(String(7), nullable=True, index=True)  # YYYY-MM формат
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    file = relationship("File", back_populates="records")

    # Индексы для быстрого поиска
    __table_args__ = (
        Index('idx_records_date_period', 'date_field', 'period'),
        Index('idx_records_file_date', 'file_id', 'date_field'),
        # Уникальность: один файл + одинаковые данные
        # UniqueConstraint('file_id', 'data', name='unique_file_data'),  # Отключено для SQLite
    )
