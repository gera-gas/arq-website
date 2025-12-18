import os
import sys
import time
import pytest
#from jose import jwt
import jwt
from datetime import timedelta
from app.auth import get_password_hash, verify_password
from app.auth import create_access_token, verify_token

# Добавляем путь к проекту для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_password_hashing():
    """Тест: хеширование пароля работает"""
    from app.auth import get_password_hash, verify_password
    
    password = "my_secure_password_123"
    hashed = get_password_hash(password)
    
    # Хеш должен быть длинным
    assert len(hashed) > 50
    
    # Проверка правильного пароля
    assert verify_password(password, hashed)
    
    # Проверка неправильного пароля
    assert not verify_password("wrong_password", hashed)
    
    # Каждый хеш должен быть уникальным
    hashed2 = get_password_hash(password)
    assert hashed != hashed2  # Argon2 добавляет случайную соль
    
    print("Hash working success!")

def test_jwt_token_creation():
    """Тест: создание JWT токена"""
    data = {"sub": "testuser", "role": "admin"}
    token = create_access_token(data)
    
    assert token is not None
    assert len(token) > 50
    print("JWT token create success!")

def test_jwt_token_verification():
    """Тест: верификация JWT токена"""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "testuser"
    print(f"payload: {payload}")
    print("JWT token verify success!")

@pytest.mark.skip
def test_expired_token():
    """Тест: просроченный токен не работает"""
    from datetime import datetime, timedelta
    from app.auth import SECRET_KEY, ALGORITHM, verify_token
    
    # Создаём токен с прошедшей датой (5 минут назад)
    expire = datetime.now() - timedelta(minutes=5)
    to_encode = {"exp": expire, "sub": "testuser"}
    expired_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    payload = verify_token(expired_token)
    print(f"Payload for expired token: {payload}")
    
    # Просроченный токен должен вернуть None
    assert payload is None
    print("Expired token dropped success!")

@pytest.mark.skip
def test_token_without_exp():
    """Тест: токен без срока истечения не проходит"""
    from app.auth import SECRET_KEY, ALGORITHM, verify_token
    
    # Токен БЕЗ поля exp
    to_encode = {"sub": "testuser"}
    token_without_exp = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    payload = verify_token(token_without_exp)
    print(f"Payload for token without exp: {payload}")
    
    # Токен без срока должен вернуть None (т.к. require_exp=True)
    assert payload is None
    print("Token without timedelta drop success!")
