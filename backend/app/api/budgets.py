from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schemas.budget import BudgetCreate, BudgetListResponse, BudgetOut
from app.services.budget import BudgetService

router = APIRouter()


@router.get("/budgets", response_model=BudgetListResponse)
def list_budgets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("id"),
    sort_dir: Literal["asc", "desc"] = Query("asc"),
    db: Session = Depends(get_db),
):
    service = BudgetService(db)
    return service.list_budgets(page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir)


@router.post("/budgets", response_model=BudgetOut, status_code=201)
def create_or_update_budget(data: BudgetCreate, db: Session = Depends(get_db)):
    service = BudgetService(db)
    return service.create_or_update_budget(data)


@router.delete("/budgets/{budget_id}", status_code=204)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    service = BudgetService(db)
    deleted = service.delete_budget(budget_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Budget not found")
