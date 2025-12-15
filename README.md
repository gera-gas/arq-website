# ARQ Website

Modern company website built with FastAPI and Tailwind CSS.

## Features
- Company presentation (landing page)
- Vacancies listing (SQLite database)
- Admin panel for vacancy management
- Responsive design for mobile/desktop

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, JWT auth
- **Frontend:** Jinja2 templates, Tailwind CSS
- **Database:** SQLite
- **Package Manager:** uv

## Quick Start

1. Clone repository
2. Set up environment:

for Linux
```bash
uv venv
source .venv/bin/activate
uv sync
```

for Windows instead `source .venv/bin/activate` run

    > .venv\Scripts\activate.bat

### **Шаг 5: Установка зависимостей**

Синхронизация зависимостей (создает uv.lock)
`uv sync`

Проверить установленные пакеты
`uv pip list`

Альтернатива: установить пакеты напрямую (без pyproject.toml)

    $ uv pip install fastapi uvicorn[standard] sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart jinja2 python-dotenv

### Project Structure

```text
arq-site/
├── app/ # Main application
├── tests/ # Test files
├── static/ # CSS, JS, images
└── alembic/ # Database migrations
```

Более подробная стрктура

```text
arq-site/
├── .venv/                     # Виртуальное окружение (uv)
├── app/
│   ├── __init__.py
│   ├── main.py               # Точка входа FastAPI
│   ├── database.py           # Настройка БД
│   ├── models.py             # SQLAlchemy модели
│   ├── schemas.py            # Pydantic схемы
│   ├── crud.py               # CRUD операции
│   ├── auth.py               # Аутентификация JWT
│   ├── dependencies.py       # Зависимости FastAPI
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── public.py         # Публичные маршруты
│   │   └── admin.py          # Админ-маршруты
│   ├── templates/            # Jinja2 шаблоны
│   └── static/               # Статические файлы
├── tests/                    # Тесты
├── alembic/                  # Миграции БД (опционально)
├── .env                      # Переменные окружения
├── .gitignore
├── pyproject.toml           # Зависимости (uv)
├── uv.lock                  # Лок файл зависимостей
└── README.md

### Server runing
Проверка через uvocorn
`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir .`

```
