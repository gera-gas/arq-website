import os
import hashlib
from passlib.context import CryptContext
from datetime import datetime, timedelta
#from jose import jwt, JWTError, ExpiredSignatureError
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# КОНФИГУРАЦИЯ ARGON2
pwd_context = CryptContext(
    schemes=["argon2"],  # Только Argon2
    argon2__time_cost=2,        # Время вычисления (больше = безопаснее, но медленнее)
    argon2__memory_cost=65536,  # Память в KiB (64MB)
    argon2__parallelism=4,      # Параллельные потоки
    deprecated="auto"
)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Создаёт хеш пароля с Argon2"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создаёт JWT токен"""
    to_encode = data.copy()
    if expires_delta:
        #expire = datetime.utcnow() + expires_delta
        expire = datetime.now() + expires_delta
    else:
        #expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Проверяет JWT токен.
    Возвращает payload если токен валиден, None если просрочен или невалиден.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require_exp": True}  # Требуем наличие поля exp
        )
        return payload
    except ExpiredSignatureError:
        # Токен просрочен
        print("Token expired!")
        return None
    except InvalidTokenError:
        print(f"InvalidTokenError")
        return None
    except PyJWTError as e:
        # Любая другая ошибка JWT (неправильная подпись, формат и т.д.)
        print(f"PyJWTError: {e}")
        return None

# Временное решение для тестов
def hash_password_stub(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password_stub(plain_password: str, hashed_password: str) -> bool:
    return hash_password_stub(plain_password) == hashed_password
