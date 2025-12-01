# VendHub Database - Backend API

FastAPI backend для VendHub Database с PostgreSQL и JWT аутентификацией.

## 🚀 Быстрый старт

### Локальная разработка

1. **Установка зависимостей:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Настройка переменных окружения:**
```bash
cp .env.example .env
# Отредактируйте .env файл
```

3. **Запуск PostgreSQL (Docker):**
```bash
docker run -d \
  --name vendhub_postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=vendhub \
  -p 5432:5432 \
  postgres:15-alpine
```

4. **Запуск приложения:**
```bash
python main.py
# или
uvicorn main:app --reload
```

5. **Открыть документацию API:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### С Docker Compose

```bash
# Из корневой директории проекта
docker-compose up -d
```

Сервисы будут доступны:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- PostgreSQL: localhost:5432

## 📊 API Endpoints

### Аутентификация

```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "user",
  "password": "password",
  "email": "user@example.com"
}
```

```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=user&password=password
```

```http
GET /api/auth/me
Authorization: Bearer {token}
```

### Файлы

```http
POST /api/files/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: <Excel файл>
```

```http
GET /api/files
Authorization: Bearer {token}
```

```http
GET /api/files/{file_id}
Authorization: Bearer {token}
```

```http
DELETE /api/files/{file_id}
Authorization: Bearer {token}
```

### Записи (База данных)

```http
GET /api/records?search=текст&period=2025-11&date_from=2025-11-01&date_to=2025-11-30&page=1&size=50
Authorization: Bearer {token}
```

```http
GET /api/records/stats
Authorization: Bearer {token}
```

```http
GET /api/records/export?period=2025-11
Authorization: Bearer {token}
```

## 🗄️ Структура базы данных

### Таблицы:

**users**
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- created_at
- updated_at

**files**
- id (Primary Key)
- user_id (Foreign Key → users.id)
- filename
- file_url
- row_count
- headers (JSONB)
- uploaded_at

**records**
- id (Primary Key)
- file_id (Foreign Key → files.id)
- data (JSONB) - данные строки
- date_field (Date) - извлеченная дата
- period (String) - период YYYY-MM
- created_at
- UNIQUE(file_id, data) - уникальность

### Индексы:

- `idx_files_user_uploaded` - быстрый поиск файлов пользователя
- `idx_records_date_period` - фильтрация по датам и периодам
- `idx_records_data_gin` - полнотекстовый поиск по JSONB
- `idx_records_file_date` - связь файл-дата

## 🔒 Безопасность

- ✅ JWT аутентификация
- ✅ Bcrypt хеширование паролей
- ✅ CORS настроен
- ✅ SQL injection защита (SQLAlchemy ORM)
- ✅ Валидация входных данных (Pydantic)
- ✅ Rate limiting (в production)

## 🌐 Деплой на Railway

1. **Установить Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Логин:**
```bash
railway login
```

3. **Создать проект:**
```bash
railway init
```

4. **Добавить PostgreSQL:**
```bash
railway add postgresql
```

5. **Деплой:**
```bash
railway up
```

6. **Настроить переменные:**
```bash
railway variables set JWT_SECRET_KEY="your-production-secret-key"
railway variables set ALLOWED_ORIGINS="https://your-domain.com"
```

7. **Получить URL:**
```bash
railway domain
```

## 📝 Переменные окружения

| Переменная | Описание | По умолчанию |
|-----------|----------|--------------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `JWT_SECRET_KEY` | Секретный ключ для JWT | - |
| `ALLOWED_ORIGINS` | CORS origins (через запятую) | `*` |
| `PORT` | Порт приложения | `8000` |
| `DEBUG` | Режим отладки | `False` |
| `LOG_LEVEL` | Уровень логирования | `INFO` |

## 🧪 Тестирование

```bash
# Установить зависимости для тестов
pip install pytest pytest-asyncio httpx

# Запустить тесты
pytest tests/

# С покрытием
pytest --cov=. tests/
```

## 📊 Мониторинг

Логи сохраняются в `logs/`:
- `vendhub_YYYY-MM-DD.log` - основные логи
- Ротация: ежедневно
- Хранение: 7 дней

## 🔧 Разработка

### Структура проекта:

```
backend/
├── main.py              # FastAPI приложение
├── database.py          # Конфигурация БД
├── models.py            # SQLAlchemy модели
├── auth.py              # JWT аутентификация
├── utils/
│   └── excel_parser.py  # Парсинг Excel
├── requirements.txt     # Зависимости
├── Dockerfile           # Docker образ
├── .env.example         # Пример конфигурации
└── README.md
```

### Добавление новых endpoints:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/custom", tags=["Custom"])

@router.get("/endpoint")
async def custom_endpoint():
    return {"message": "Custom endpoint"}

# В main.py:
app.include_router(router)
```

## 🐛 Troubleshooting

### Database connection errors:
```bash
# Проверить статус PostgreSQL
docker ps | grep postgres

# Посмотреть логи
docker logs vendhub_postgres

# Пересоздать контейнер
docker-compose down -v
docker-compose up -d
```

### JWT errors:
- Проверьте `JWT_SECRET_KEY` в .env
- Убедитесь что ключ минимум 32 символа

### CORS errors:
- Добавьте домен в `ALLOWED_ORIGINS`
- Проверьте порты (backend: 8000, frontend: 3000)

## 📚 Документация

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Railway Deploy](https://docs.railway.app/)

## 🤝 Contributing

1. Fork проект
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Открытьте Pull Request

## 📄 License

MIT License - смотрите LICENSE файл

## 👨‍💻 Author

VendHub Team - [https://vendhub.com](https://vendhub.com)
