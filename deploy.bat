@echo off
echo ========================================
echo VendHub Database - Деплой на Railway
echo ========================================
echo.

REM Проверка git
git --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Git не установлен!
    echo Скачайте и установите Git: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Проверка Git репозитория...
if not exist ".git" (
    echo Инициализация Git репозитория...
    git init
    echo Git репозиторий создан!
) else (
    echo Git репозиторий уже существует.
)

echo.
echo [2/5] Настройка .gitignore...
if not exist ".gitignore" (
    echo __pycache__/ > .gitignore
    echo *.pyc >> .gitignore
    echo .env >> .gitignore
    echo *.db >> .gitignore
    echo vendhub.db >> .gitignore
    echo .DS_Store >> .gitignore
    echo .vscode/ >> .gitignore
    echo node_modules/ >> .gitignore
    echo uploads/ >> .gitignore
    echo logs/ >> .gitignore
    echo .gitignore создан!
) else (
    echo .gitignore уже существует.
)

echo.
echo [3/5] Генерация JWT Secret Key...
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))" > .railway_secret.txt
echo Секретный ключ сохранен в .railway_secret.txt
echo.
type .railway_secret.txt
echo.
echo ВАЖНО: Сохраните этот ключ! Он понадобится в Railway Variables.
echo.

echo [4/5] Добавление файлов в Git...
git add .
echo Файлы добавлены.

echo.
set /p commit_msg="Введите сообщение коммита (или нажмите Enter для 'Initial commit'): "
if "%commit_msg%"=="" set commit_msg=Initial commit: VendHub Database

git commit -m "%commit_msg%"
echo Коммит создан!

echo.
echo [5/5] Готово к отправке на GitHub!
echo.
echo ========================================
echo Следующие шаги:
echo ========================================
echo.
echo 1. Создайте репозиторий на GitHub:
echo    https://github.com/new
echo.
echo 2. Выполните команды (замените USERNAME на ваш логин):
echo    git remote add origin https://github.com/USERNAME/vendhub-database.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Перейдите на Railway:
echo    https://railway.app
echo.
echo 4. Создайте новый проект из вашего GitHub репозитория
echo.
echo 5. Добавьте PostgreSQL database в проект
echo.
echo 6. Настройте Variables (скопируйте из .railway_secret.txt):
type .railway_secret.txt
echo    ALLOWED_ORIGINS=*
echo    PORT=8000
echo    DEBUG=False
echo.
echo 7. Подождите завершения деплоя и получите ваш URL!
echo.
echo Полная инструкция: QUICK_DEPLOY.md
echo.
pause
