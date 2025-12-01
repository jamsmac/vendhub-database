# 🚀 Руководство по развертыванию VendHub Database

Полная инструкция по развертыванию online-версии VendHub Database с работой 24/7.

## 📋 Содержание

1. [Локальная разработка](#локальная-разработка)
2. [Деплой на Railway](#деплой-на-railway)
3. [Деплой Frontend](#деплой-frontend)
4. [Настройка домена](#настройка-домена)
5. [Troubleshooting](#troubleshooting)

---

## 🏠 Локальная разработка

### Предварительные требования:

- Python 3.11+
- PostgreSQL 15+
- Docker (опционально)

### Быстрый старт с Docker Compose:

```bash
# 1. Перейти в корень проекта
cd 011225

# 2. Запустить все сервисы
docker-compose up -d

# 3. Проверить статус
docker-compose ps

# 4. Просмотреть логи
docker-compose logs -f backend
```

**Доступ:**
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Ручная установка:

#### Backend:

```bash
# 1. Установка зависимостей
cd backend
pip install -r requirements.txt

# 2. Настройка .env
cp .env.example .env
# Отредактировать .env файл

# 3. Запуск PostgreSQL
docker run -d \
  --name vendhub_postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=vendhub \
  -p 5432:5432 \
  postgres:15-alpine

# 4. Запуск приложения
python main.py
```

#### Frontend:

```bash
# Просто откройте vendhub_simple.html в браузере
# Или используйте простой HTTP сервер:
python -m http.server 3000
```

---

## ☁️ Деплой на Railway

### Вариант 1: Через Railway CLI

```bash
# 1. Установка Railway CLI
npm install -g @railway/cli

# 2. Логин
railway login

# 3. Создание проекта
railway init

# 4. Добавление PostgreSQL
railway add

# Выберите: PostgreSQL

# 5. Деплой backend
cd backend
railway up

# 6. Настройка переменных окружения
railway variables set JWT_SECRET_KEY="your-super-secret-key-min-32-characters"
railway variables set ALLOWED_ORIGINS="https://your-frontend-domain.com"

# 7. Получить URL
railway domain
```

### Вариант 2: Через GitHub Integration

1. **Создать репозиторий на GitHub:**
```bash
git init
git add .
git commit -m "Initial commit: VendHub Database online version"
git remote add origin https://github.com/yourusername/vendhub.git
git push -u origin main
```

2. **В Railway Dashboard:**
   - New Project → Deploy from GitHub
   - Выбрать репозиторий
   - Root Directory: `backend`
   - Deploy

3. **Добавить PostgreSQL:**
   - В проекте → New → Database → PostgreSQL
   - Railway автоматически добавит `DATABASE_URL`

4. **Настроить переменные:**
   - Variables tab →
   - `JWT_SECRET_KEY` = `your-secret-key`
   - `ALLOWED_ORIGINS` = `https://your-domain.com`
   - `PORT` = `8000`

5. **Настроить домен:**
   - Settings → Generate Domain
   - Или добавить свой домен

### Вариант 3: Через Railway Web Interface

1. **Перейти на [railway.app](https://railway.app)**
2. **New Project → Empty Project**
3. **Add Service → Database → PostgreSQL**
4. **Add Service → GitHub Repo** (или Deploy from template)
5. **Выбрать backend директорию**
6. **Настроить переменные окружения**
7. **Deploy!**

---

## 🌐 Деплой Frontend

### Cloudflare Pages (рекомендуется):

```bash
# 1. Установка Wrangler CLI
npm install -g wrangler

# 2. Логин
wrangler login

# 3. Создать проект Pages
wrangler pages project create vendhub-frontend

# 4. Деплой
cd frontend
wrangler pages publish . --project-name=vendhub-frontend

# 5. Настроить переменные окружения
# В Cloudflare Dashboard → Pages → Settings → Environment variables:
# API_URL = https://your-backend-url.railway.app
```

### Vercel:

```bash
# 1. Установка Vercel CLI
npm install -g vercel

# 2. Деплой
cd frontend
vercel

# 3. Настроить переменные окружения в Vercel Dashboard
```

### Netlify:

```bash
# 1. Установка Netlify CLI
npm install -g netlify-cli

# 2. Деплой
cd frontend
netlify deploy --prod

# 3. Настроить переменные окружения в Netlify Dashboard
```

### Простой вариант - GitHub Pages:

```bash
# 1. Создать репозиторий на GitHub
# 2. Скопировать frontend файлы в gh-pages branch
git checkout -b gh-pages
git add frontend/*
git commit -m "Deploy frontend"
git push origin gh-pages

# 3. В Settings → Pages → выбрать gh-pages branch
```

---

## 🔐 Настройка домена

### Railway Custom Domain:

1. Railway Dashboard → Settings → Networking
2. Add Custom Domain: `api.vendhub.com`
3. Добавить CNAME запись у DNS провайдера:
   ```
   CNAME api.vendhub.com → your-project.railway.app
   ```

### Cloudflare Custom Domain:

1. Cloudflare Dashboard → Pages → Custom domains
2. Add domain: `vendhub.com`
3. Cloudflare автоматически настроит DNS

### SSL Certificate:

- Railway/Cloudflare предоставляют бесплатные SSL сертификаты
- Автоматическое обновление

---

## 🔄 Обновление приложения

### Railway:

```bash
# Через Git
git add .
git commit -m "Update features"
git push

# Railway автоматически задеплоит новую версию

# Или через CLI
railway up
```

### Frontend:

```bash
# Cloudflare Pages
wrangler pages publish .

# Vercel
vercel --prod

# Netlify
netlify deploy --prod
```

---

## 📊 Мониторинг

### Railway:

- **Логи:** Railway Dashboard → Deployments → Logs
- **Метрики:** Dashboard → Metrics
- **Health checks:** Автоматически

### Мониторинг ошибок (опционально):

```bash
# Установить Sentry
pip install sentry-sdk

# В main.py:
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

### Uptime мониторинг:

- [UptimeRobot](https://uptimerobot.com/) - бесплатно
- [StatusCake](https://www.statuscake.com/) - бесплатно
- [Pingdom](https://www.pingdom.com/)

---

## 💰 Стоимость

### Бесплатный вариант (Hobby):

| Сервис | Стоимость | Лимиты |
|--------|----------|---------|
| Railway Starter | $0 | $5 credits/месяц |
| PostgreSQL | включено | 1GB |
| Cloudflare Pages | $0 | Unlimited |
| **Итого** | **$0-5/мес** | Подходит для малых проектов |

### Профессиональный вариант:

| Сервис | Стоимость | Лимиты |
|--------|----------|---------|
| Railway Pro | $20/мес | Более мощные ресурсы |
| PostgreSQL | включено | 8GB + backups |
| Cloudflare Pages | $0 | Unlimited |
| Domain (.com) | $12/год | - |
| **Итого** | **~$35/мес** | Production-ready |

---

## 🐛 Troubleshooting

### Backend не запускается:

```bash
# Проверить логи
railway logs

# Проверить переменные окружения
railway variables

# Проверить DATABASE_URL
echo $DATABASE_URL
```

### Frontend не подключается к Backend:

1. Проверить CORS в backend:
   ```python
   # backend/main.py
   ALLOWED_ORIGINS = ["https://your-frontend.pages.dev"]
   ```

2. Проверить API_URL в frontend:
   ```javascript
   const API_URL = 'https://your-backend.railway.app';
   ```

### Database connection errors:

```bash
# Пересоздать PostgreSQL
railway down
railway add postgresql

# Или подключиться вручную
psql $DATABASE_URL
```

### 502/503 errors:

- Проверить healthcheck: `/health`
- Увеличить память в Railway Settings
- Проверить логи на ошибки

### Медленная работа:

```python
# Добавить Redis для кэширования
# В Railway: Add → Redis

# backend/main.py
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="vendhub:")
```

---

## 📚 Полезные ссылки

- [Railway Docs](https://docs.railway.app/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Cloudflare Pages](https://pages.cloudflare.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## 🔒 Безопасность в Production

### Обязательные шаги:

1. **Изменить JWT_SECRET_KEY:**
   ```bash
   # Генерация безопасного ключа
   openssl rand -hex 32
   ```

2. **Настроить CORS:**
   ```python
   ALLOWED_ORIGINS = [
       "https://vendhub.com",
       "https://www.vendhub.com"
   ]
   ```

3. **Rate limiting:**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)

   @app.post("/api/auth/login")
   @limiter.limit("5/minute")
   async def login(...):
       ...
   ```

4. **HTTPS только:**
   - Railway/Cloudflare предоставляют автоматически

5. **Бэкапы БД:**
   ```bash
   # Railway автоматически делает бэкапы
   # Или настроить ручные:
   pg_dump $DATABASE_URL > backup.sql
   ```

---

## ✅ Чеклист деплоя

- [ ] Backend развернут на Railway
- [ ] PostgreSQL добавлена и подключена
- [ ] JWT_SECRET_KEY установлен (минимум 32 символа)
- [ ] ALLOWED_ORIGINS настроены
- [ ] Frontend развернут на Cloudflare Pages
- [ ] API_URL в frontend указывает на Railway
- [ ] Домен настроен (опционально)
- [ ] SSL работает (HTTPS)
- [ ] Health check работает: `/health`
- [ ] Первый пользователь создан
- [ ] Тестовый файл загружен успешно
- [ ] Экспорт данных работает
- [ ] Uptime monitoring настроен

---

## 🎉 Готово!

Ваше приложение VendHub Database развернуто и работает 24/7!

**API URL:** https://your-project.railway.app
**Frontend URL:** https://your-project.pages.dev
**API Docs:** https://your-project.railway.app/docs

### Первые шаги:

1. **Создать пользователя:**
   ```bash
   curl -X POST "https://your-api.railway.app/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"secure_password","email":"admin@vendhub.com"}'
   ```

2. **Получить токен:**
   ```bash
   curl -X POST "https://your-api.railway.app/api/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=secure_password"
   ```

3. **Загрузить первый файл через UI**

---

## 📞 Поддержка

Возникли проблемы?
- Проверьте логи в Railway Dashboard
- Посмотрите Issues на GitHub
- Напишите на support@vendhub.com

**Happy deploying! 🚀**
