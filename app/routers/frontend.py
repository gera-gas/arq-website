import os
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(include_in_schema=False)  # Не показывать в Swagger

# Указываем папку с шаблонами
templates = Jinja2Templates(directory="app/templates")
# DEBUG!
# print(f"🛠️  Templates directory: {templates}")

@router.get("/")
async def home(request: Request):
    """
    Главная страница сайта.
    
    Args:
        request: HTTP запрос (обязательный параметр для Jinja2)
    
    Returns:
        TemplateResponse: Отрендеренный HTML шаблон
        
    Note:
        - 'request' всегда передаём в шаблон (требование Jinja2)
        - 'active_page' используется для подсветки активной ссылки в навигации
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "active_page": "home",
            "title": "ARQ - IT Solutions",
            "company_name": "ARQ"
        }
    )

@router.get("/vacancies")
async def vacancies_page(request: Request):
    """
    Обработчик страницы вакансий.
    Пока заглушка, позже добавим данные из БД.
    """
    return templates.TemplateResponse(
        request=request,
        name="vacancies.html",  # Создадим позже
        context={
            "active_page": "vacancies",
            "title": "ARQ - Вакансии",
            "vacancies": []  # Пока пустой список
        }
    )

@router.get("/directions")
async def directions_page(request: Request):
        return templates.TemplateResponse(
            request=request,
            name="directions.html",  # Создадим позже
            context={
                "active_page": "directions",
                "title": "ARQ - Направления",
            }
        )
