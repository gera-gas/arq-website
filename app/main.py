from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.routers import frontend

# app = FastAPI(title="ARQ Professional")
app = FastAPI(
    title="ARQ",
    description="Company website with vacancies management",
    version="0.1.0",
)

# Подключаем роутеры
app.include_router(frontend.router)  # HTML страницы
# app.include_router(api.router)     # API endpoints (позже)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

