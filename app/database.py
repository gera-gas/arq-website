# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Загружаем переменные из .env файла
#    Если .env нет - используем значения по умолчанию
load_dotenv(".env.local")
# Затем общие (они не заменят уже загруженные из .env.local)
load_dotenv(".env", override=True)

# 2. URL подключения к базе данных
#    Формат: dialect+driver://username:password@host:port/database
#    Для SQLite: sqlite:///./filename.db
#    Для PostgreSQL: postgresql://user:password@localhost/arq_db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./arq.db")

# 3. Создаём "движок" - основной объект для работы с БД
#    connect_args нужен ТОЛЬКО для SQLite
engine = create_engine(
    DATABASE_URL,
    # Для SQLite нужно отключить проверку одного потока
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    # Показываем SQL-запросы в консоли (удобно для отладки)
    echo=True  # УБЕРИ В ПРОДАКШЕНЕ!
)

# 4. SessionLocal - фабрика для создания сессий БД
#    Сессия = временное подключение к БД для группы операций
SessionLocal = sessionmaker(
    autocommit=False,  # Не коммитить автоматически
    autoflush=False,   # Не сбрасывать изменения в БД автоматически
    bind=engine        # Привязываем к нашему движку
)

# 5. Base - базовый класс для всех моделей (таблиц)
#    От него наследуются все классы моделей
Base = declarative_base()

# 6. Функция для получения сессии БД
#    Используется как dependency в FastAPI
def get_db():
    """
    Генератор сессии БД.
    FastAPI будет вызывать эту функцию для каждого запроса,
    а после завершения запроса - закрывать сессию.
    """
    db = SessionLocal()  # Создаём новую сессию
    try:
        yield db  # Отдаём сессию в обработчик запроса
    finally:
        db.close()  # Закрываем сессию в любом случае (даже если была ошибка)

# 7. Функция для инициализации БД (создание таблиц)
def init_db():
    """
    Создаёт все таблицы в базе данных.
    Вызывается при старте приложения.
    """
    print("Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы успешно!")
