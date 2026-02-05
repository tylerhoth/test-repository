from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schemas.dashboard import (
    DashboardSummary,
    IncomeVsExpensesResponse,
    RecurringChargesResponse,
    SpendingByCategoryResponse,
)
from app.services.dashboard import DashboardService

router = APIRouter()


@router.get("/dashboard/summary", response_model=DashboardSummary)
def get_summary(db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.get_summary()


@router.get("/dashboard/spending-by-category", response_model=SpendingByCategoryResponse)
def spending_by_category(db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.spending_by_category()


@router.get("/dashboard/income-vs-expenses", response_model=IncomeVsExpensesResponse)
def income_vs_expenses(db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.income_vs_expenses()


@router.get("/dashboard/recurring", response_model=RecurringChargesResponse)
def recurring_charges(db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.recurring_charges()
