"""
Конфигурация базы данных PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# Загружаем .env только если файл существует (для локальной разработки)
if os.path.exists(".env"):
    load_dotenv()

# Database URL из переменных окружения
# Railway автоматически предоставляет DATABASE_URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/vendhub"
)

# Исправление DATABASE_URL для Railway (если используется postgres:// вместо postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Создание engine с пулом соединений
# Добавляем connect_args для лучшей обработки ошибок
connect_args = {}
# Railway PostgreSQL обычно требует SSL, но не всегда
# Если в URL уже есть sslmode, не переопределяем
if "sslmode" not in DATABASE_URL.lower():
    # Пробуем prefer (не требует, но использует если доступно)
    connect_args = {"sslmode": "prefer"}

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    echo=False,  # Логирование SQL запросов (для дебага)
    connect_args=connect_args,
    # Увеличиваем таймауты для Railway
    pool_recycle=3600,  # Переподключение каждый час
    pool_timeout=30,  # Таймаут ожидания соединения
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
    from passlib.context import CryptContext

    try:
        # Проверка подключения к БД
        print("Attempting to connect to the database...")
        print(f"Database URL: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else '***'}")
        
        # Тестовое подключение
        with engine.connect() as conn:
            print("✓ Database connection successful!")
        
        # Создание таблиц
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created/verified")
        
        # Создание админа только если его нет
        db = SessionLocal()
        try:
            from models import User

            # Проверяем, есть ли админ
            admin = db.query(User).filter(User.username == "jamshiddin").first()

            if not admin:
                # Создаем админа
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                admin_user = User(
                    username="jamshiddin",
                    email="admin@vendhub.com",
                    password_hash=pwd_context.hash("311941990")
                )
                db.add(admin_user)
                db.commit()
                print("✓ Admin user 'jamshiddin' created successfully")
            else:
                print("✓ Admin user already exists")
        except Exception as e:
            print(f"✗ Admin creation error: {e}")
            db.rollback()
            raise
        finally:
            db.close()
            
    except Exception as e:
        error_msg = str(e)
        print(f"✗ Database connection failed: {error_msg}")
        print("\nTroubleshooting steps:")
        print("1. Check DATABASE_URL in Railway variables")
        print("2. Verify PostgreSQL service is running")
        print("3. Check network connectivity")
        print("4. Review Railway logs for more details")
        raise
