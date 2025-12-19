"""
Скрипт для инициализации базы данных.
Запускается один раз при первом запуске проекта.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import Vacancy, AdminUser
from passlib.context import CryptContext

def init_database():
    """Создаёт таблицы и тестовые данные"""
    print("Create tqables...")
    Base.metadata.create_all(bind=engine)
    print("Tables was created.")
    
    # Проверь, что таблицы создались
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables: {tables}")

def create_test_data():
    """Создаёт тестовые данные для разработки"""
    from app.database import SessionLocal
    from sqlalchemy.exc import IntegrityError
    
    db = SessionLocal()
    #pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    from app.auth import get_password_hash
    
    try:
        # Создаём тестового администратора
        admin_exists = db.query(AdminUser).filter_by(username="admin").first()
        if not admin_exists:
            print("\nNo admin found in database!")
            print("Please create first administrator:")
            username = input("Username [admin]: ").strip() or "admin"
            password = input("Password [admin123]: ").strip() or "admin123"
            admin = AdminUser(
                username="username",
                hashed_password=get_password_hash(password)
                #hashed_password=hash_password_stub("admin123")
                #hashed_password=pwd_context.hash("admin123")  # Смени в продакшене!
            )
            db.add(admin)
            print("Create test admin: admin/admin123")
        
        # Создаём тестовые вакансии
        vacancies = [
            Vacancy(
                title="Python Backend Developer",
                description="Разработка на FastAPI и SQLAlchemy",
                requirements="Python 3.9+, FastAPI, SQLAlchemy, PostgreSQL",
                is_active=True
            ),
            Vacancy(
                title="Frontend Developer",
                description="Разработка пользовательских интерфейсов",
                requirements="JavaScript, React/Vue, HTML/CSS",
                is_active=True
            ),
            Vacancy(
                title="Embedded Engineer",
                description="Разработка встроенных систем",
                requirements="C/C++, Python, FPGA, PCB design",
                is_active=False  # Неактивная вакансия
            )
        ]
        
        for vacancy in vacancies:
            exists = db.query(Vacancy).filter_by(title=vacancy.title).first()
            if not exists:
                db.add(vacancy)
        
        db.commit()
        print(f"Create {len(vacancies)} tests vecencies")
        
    except IntegrityError as e:
        db.rollback()
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Initialize of ARQ database...")
    init_database()
    create_test_data()
    print("Done! Database was initialized success.")
