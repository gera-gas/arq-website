from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

app = FastAPI(
    title="ARQ",
    description="Company website with vacancies management",
    version="0.1.0",
)

@app.get("/")
async def home():
    return {"message": "Hello ARQ!", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
