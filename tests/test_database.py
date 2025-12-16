import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Добавляем путь к проекту для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, get_db
from app.models import Vacancy, AdminUser

# Тестовая база данных в памяти (не сохраняется на диск)
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """
    Фикстура: создаёт чистую тестовую БД для каждого теста.
    scope="function" - БД создаётся заново для каждого теста.
    """
    # Создаём движок для тестовой БД
    engine = create_engine(TEST_DATABASE_URL)
    # Создаём все таблицы
    Base.metadata.create_all(bind=engine)
    # Создаём сессию
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db  # Отдаём БД в тест
    finally:
        db.close()  # Закрываем соединение

def test_database_connection(test_db):
    """Тест: подключение к БД работает"""
    # Простой запрос к БД
    result = test_db.execute("SELECT 1").fetchone()
    assert result[0] == 1
    print("DB connection test: success!")

def test_create_vacancy(test_db):
    """Тест: создание вакансии в БД"""
    # Создаём объект вакансии
    vacancy = Vacancy(
        title="Python developer",
        description="Developing on FastAPI и SQLAlchemy",
        requirements="Python 3.9+, FastAPI, SQLAlchemy",
        is_active=True
    )
    # Добавляем в БД
    test_db.add(vacancy)
    test_db.commit()  # Сохраняем изменения
    test_db.refresh(vacancy)  # Обновляем объект (получаем ID)
    # Проверяем, что вакансия создана
    assert vacancy.id is not None
    assert vacancy.title == "Python developer"
    assert vacancy.is_active == True
    
    print(f"Vacancy created: ID={vacancy.id}, Title={vacancy.title}")

def test_read_vacancy(test_db):
    """Тест: чтение вакансии из БД"""
    # Сначала создаём тестовую вакансию
    vacancy = Vacancy(
        title="Frontend developer",
        description="UI/UX design and implementation",
        is_active=True
    )
    test_db.add(vacancy)
    test_db.commit()
    # Читаем вакансию из БД
    found_vacancy = test_db.query(Vacancy).filter_by(title="Frontend developer").first()
    # Проверяем, что нашли правильную вакансию
    assert found_vacancy is not None
    assert found_vacancy.description == "UI/UX design and implementation"
    
    print(f"Vacancy read: {found_vacancy.title}")

def test_update_vacancy(test_db):
    """Тест: обновление вакансии в БД"""
    # Создаём вакансию
    vacancy = Vacancy(
        title="Old vacancy",
        description="Old description",
        is_active=True
    )
    test_db.add(vacancy)
    test_db.commit()
    test_db.refresh(vacancy)
    # Обновляем вакансию
    vacancy.title = "New vacancy"
    vacancy.is_active = False
    test_db.commit()
    test_db.refresh(vacancy)
    
    # Проверяем обновление
    updated_vacancy = test_db.query(Vacancy).get(vacancy.id)
    assert updated_vacancy.title == "New vacancy"
    assert updated_vacancy.is_active == False
    
    print(f"Vacancy updated: {updated_vacancy.title}")

def test_delete_vacancy(test_db):
    """Тест: удаление вакансии из БД"""
    # Создаём вакансию
    vacancy = Vacancy(
        title="Deleted vacancy",
        description="Will be delete",
        is_active=True
    )
    test_db.add(vacancy)
    test_db.commit()
    # Удаляем вакансию
    test_db.delete(vacancy)
    test_db.commit()
    # Проверяем, что вакансии больше нет
    deleted_vacancy = test_db.query(Vacancy).filter_by(title="Deleted vacancy").first()
    assert deleted_vacancy is None
    
    print("Vacancy deletion success!")

def test_create_admin_user(test_db):
    """Тест: создание администратора"""
    # Импортируем функцию хеширования паролей
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # Создаём администратора
    admin = AdminUser(
        username="testadmin",
        hashed_password=pwd_context.hash("testpassword123")
    )
    test_db.add(admin)
    test_db.commit()
    test_db.refresh(admin)
    # Проверяем создание
    assert admin.id is not None
    assert admin.username == "testadmin"
    # Проверяем хеш пароля
    assert pwd_context.verify("testpassword123", admin.hashed_password)
    
    print(f"Admin created: {admin.username}")

def test_crud_operations_flow(test_db):
    """Тест: полный цикл CRUD операций"""
    # Create
    vacancy = Vacancy(title="Full Stack", description="Full cycle", is_active=True)
    test_db.add(vacancy)
    test_db.commit()
    # Read
    found = test_db.query(Vacancy).filter_by(title="Full Stack").first()
    assert found is not None
    # Update
    found.description = "Updated description"
    test_db.commit()
    # Delete
    test_db.delete(found)
    test_db.commit()
    # Verify delete
    deleted = test_db.query(Vacancy).filter_by(title="Full Stack").first()
    assert deleted is None
    
    print("Full cycle of CRUD: success!")

if __name__ == "__main__":
    """
    Запуск тестов без pytest (для отладки)
    """
    import tempfile
    
    # Создаём временную БД на диске для отладки
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    # Переопределяем DATABASE_URL
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    # Импортируем и инициализируем БД
    from app.database import init_db
    init_db()    
    print("DB tests run...")
    # Создаём тестовую сессию
    from app.database import engine, SessionLocal
    db = SessionLocal()
    try:
        # Запускаем тесты вручную
        test_database_connection(db)
        test_create_vacancy(db)
        test_read_vacancy(db)
        test_update_vacancy(db)
        test_delete_vacancy(db)
        test_create_admin_user(db)
        test_crud_operations_flow(db)
        print("\nAll tests success!")
    except Exception as e:
        print(f"\nTests error: {e}")
    finally:
        db.close()
        # Удаляем временную БД
        if os.path.exists(db_path):
            os.unlink(db_path)
