from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.todos import router as todos_router

app = FastAPI(title="Fullstack Starter API", version="0.1.0")

app.include_router(health_router)
app.include_router(todos_router, prefix="/api")
