from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.accounts import router as accounts_router
from app.api.budgets import router as budgets_router
from app.api.categories import router as categories_router
from app.api.category_rules import router as category_rules_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router
from app.api.insights import router as insights_router
from app.api.labels import router as labels_router
from app.api.todos import router as todos_router
from app.api.transactions import router as transactions_router

app = FastAPI(title="CashLens API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(todos_router, prefix="/api")
app.include_router(accounts_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(transactions_router, prefix="/api")
app.include_router(category_rules_router, prefix="/api")
app.include_router(budgets_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(insights_router, prefix="/api")
app.include_router(labels_router, prefix="/api")
