# 🗃️ VendHub Database - Online Version

Полнофункциональная система управления базой данных VendHub с работой 24/7, реальной базой данных PostgreSQL и многопользовательским доступом.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Возможности

### 📊 Управление данными
- ✅ Загрузка Excel файлов (.xlsx, .xls)
- ✅ Автоматическое распознавание структуры таблиц
- ✅ Дедупликация записей (только уникальные данные)
- ✅ Накопительная база данных
- ✅ Группировка по датам и месяцам

### 🔍 Мощные фильтры
- ✅ Полнотекстовый поиск по всем полям
- ✅ Фильтрация по периодам (месяц/год)
- ✅ Фильтрация по диапазону дат
- ✅ Сортировка по любым колонкам
- ✅ Пагинация (50/100/250/500 записей)

### 💾 Экспорт и отчеты
- ✅ Экспорт отфильтрованных данных в Excel
- ✅ Статистика по базе данных
- ✅ Группировка данных по месяцам
- ✅ История загруженных файлов

### 👥 Многопользовательский доступ
- ✅ Регистрация и аутентификация (JWT)
- ✅ Каждый пользователь видит только свои данные
- ✅ Безопасное хранение паролей (bcrypt)
- ✅ Session management

### 🎨 Современный UI
- ✅ Красивый адаптивный интерфейс
- ✅ Темная/светлая тема
- ✅ Drag & Drop загрузка файлов
- ✅ Модальные окна для просмотра файлов
- ✅ Toast уведомления

### ⚡ Производительность
- ✅ Оптимизированные SQL запросы
- ✅ GIN индексы для полнотекстового поиска
- ✅ Пул соединений с базой данных
- ✅ Асинхронная обработка запросов

## 🚀 Быстрый старт

### Локально с Docker:

```bash
# 1. Клонировать репозиторий
git clone https://github.com/jamsmac/vendhub-database.git
cd vendhub-database

# 2. Запустить все сервисы
docker-compose up -d

# 3. Открыть в браузере
# Backend API: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Ручная установка:

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Отредактировать .env
python main.py

# Frontend
# Открыть vendhub_simple.html в браузере
```

## 📁 Структура проекта

```
011225/
├── backend/                    # FastAPI Backend
│   ├── main.py                 # Основное приложение
│   ├── models.py               # SQLAlchemy модели
│   ├── database.py             # Конфигурация БД
│   ├── auth.py                 # JWT аутентификация
│   ├── utils/
│   │   └── excel_parser.py     # Парсинг Excel
│   ├── requirements.txt        # Python зависимости
│   ├── Dockerfile              # Docker образ
│   ├── .env.example            # Пример конфигурации
│   └── README.md               # Backend документация
├── frontend/                   # Frontend (в разработке)
│   └── vendhub_simple.html     # Текущая версия
├── docker-compose.yml          # Docker Compose конфигурация
├── DEPLOYMENT.md               # Руководство по деплою
└── README.md                   # Этот файл
```

## 🗄️ База данных

### Таблицы:

**users** - Пользователи системы
- id, username, email, password_hash
- created_at, updated_at

**files** - Загруженные Excel файлы
- id, user_id, filename, file_url
- row_count, headers (JSONB)
- uploaded_at

**records** - Записи из файлов
- id, file_id, data (JSONB)
- date_field, period
- created_at
- UNIQUE(file_id, data) - гарантия уникальности

### Оптимизация:

- GIN индекс для полнотекстового поиска в JSONB
- Composite индексы для фильтрации по датам
- Connection pooling для производительности

## 🔐 API

### Аутентификация:

```bash
# Регистрация
POST /api/auth/register
{
  "username": "user",
  "password": "password",
  "email": "user@example.com"
}

# Вход
POST /api/auth/login
username=user&password=password

# Ответ:
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Работа с файлами:

```bash
# Загрузка Excel файла
POST /api/files/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

# Список файлов
GET /api/files
Authorization: Bearer <token>

# Удаление файла
DELETE /api/files/{id}
Authorization: Bearer <token>
```

### База данных:

```bash
# Получить записи с фильтрами
GET /api/records?search=текст&period=2025-11&page=1&size=50
Authorization: Bearer <token>

# Статистика
GET /api/records/stats
Authorization: Bearer <token>

# Экспорт
GET /api/records/export?period=2025-11
Authorization: Bearer <token>
```

### API документация:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🌐 Деплой

### Railway (рекомендуется):

```bash
# 1. Установить CLI
npm install -g @railway/cli

# 2. Логин и деплой
railway login
railway init
railway add postgresql
cd backend && railway up

# 3. Настроить переменные окружения
railway variables set JWT_SECRET_KEY="your-secret"
railway variables set ALLOWED_ORIGINS="https://your-domain.com"
```

### Другие платформы:

- ✅ **Railway** - рекомендуется, простой деплой
- ✅ **Render** - хорошая альтернатива
- ✅ **Heroku** - классика
- ✅ **AWS/GCP/Azure** - для enterprise
- ✅ **VPS** - полный контроль

Подробнее: [DEPLOYMENT.md](./DEPLOYMENT.md)

## 💰 Стоимость хостинга

### Бесплатный вариант:
- Railway Starter: $0-5/мес
- Cloudflare Pages: $0
- **Итого: $0-5/месяц**

### Production вариант:
- Railway Pro: $20/мес
- Cloudflare Pages: $0
- Domain: $12/год
- **Итого: ~$35/месяц**

## 🔧 Настройка

### Backend (.env):

```env
DATABASE_URL=postgresql://user:pass@host:5432/vendhub
JWT_SECRET_KEY=your-super-secret-key-32-chars-minimum
ALLOWED_ORIGINS=http://localhost:3000,https://vendhub.com
PORT=8000
DEBUG=False
```

### Frontend:

```javascript
// Конфигурация API в HTML
const API_URL = 'https://your-backend.railway.app';
```

## 📊 Производительность

### Benchmarks (локально):

- Загрузка файла 1000 строк: ~500ms
- Поиск в 10,000 записей: ~100ms
- Экспорт 5,000 записей: ~800ms
- Регистрация пользователя: ~200ms

### Оптимизации:

- ✅ PostgreSQL connection pooling
- ✅ GIN индексы для JSONB
- ✅ Пагинация везде
- ✅ Асинхронные операции
- ⏳ Redis кэширование (planned)
- ⏳ CDN для статики (planned)

## 🧪 Тестирование

```bash
cd backend

# Установить зависимости для тестов
pip install pytest pytest-asyncio httpx

# Запустить тесты
pytest tests/

# С покрытием
pytest --cov=. tests/
```

## 📚 Документация

- [Backend README](./backend/README.md) - Подробная документация API
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Руководство по деплою
- [API Docs](http://localhost:8000/docs) - Swagger UI (после запуска)

## 🤝 Вклад в проект

Мы приветствуем ваш вклад!

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменений (`git commit -m 'Add AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 🐛 Сообщить об ошибке

Нашли баг? [Создайте issue](https://github.com/jamsmac/vendhub-database/issues)

## 📝 TODO / Roadmap

### v1.1 (Планируется):
- [ ] Онлайн версия frontend с API клиентом
- [ ] WebSocket для реал-тайм обновлений
- [ ] Redis кэширование
- [ ] Bulk операции (массовая загрузка)
- [ ] Расширенная аналитика

### v1.2 (Будущее):
- [ ] Права доступа и роли
- [ ] Sharing файлов между пользователями
- [ ] REST API webhooks
- [ ] Интеграция с внешними сервисами
- [ ] Mobile app (React Native)

## 📜 Лицензия

MIT License - см. [LICENSE](./LICENSE)

## 👨‍💻 Авторы

**VendHub Team**
- Website: [https://vendhub.com](https://vendhub.com)
- Email: support@vendhub.com
- GitHub: [@vendhub](https://github.com/vendhub)

## 🙏 Благодарности

- [FastAPI](https://fastapi.tiangolo.com/) - за отличный фреймворк
- [PostgreSQL](https://www.postgresql.org/) - за надежную БД
- [Railway](https://railway.app/) - за простой деплой
- [Cloudflare](https://www.cloudflare.com/) - за CDN и Pages

---

## 📞 Поддержка

Нужна помощь?

- 📖 [Документация](./DEPLOYMENT.md)
- 💬 [Discussions](https://github.com/jamsmac/vendhub-database/discussions)
- 🐛 [Issues](https://github.com/jamsmac/vendhub-database/issues)
- 📧 [Email](mailto:support@vendhub.com)

---

<p align="center">
  Сделано с ❤️ командой VendHub
</p>

<p align="center">
  <a href="#-возможности">Возможности</a> •
  <a href="#-быстрый-старт">Быстрый старт</a> •
  <a href="#-деплой">Деплой</a> •
  <a href="#-документация">Документация</a>
</p>
