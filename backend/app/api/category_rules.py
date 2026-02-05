from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schemas.category_rule import CategoryRuleCreate, CategoryRuleListResponse, CategoryRuleOut
from app.services.category_rule import CategoryRuleService

router = APIRouter()


@router.get("/category-rules", response_model=CategoryRuleListResponse)
def list_rules(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort_by: str = Query("id"),
    sort_dir: Literal["asc", "desc"] = Query("asc"),
    db: Session = Depends(get_db),
):
    service = CategoryRuleService(db)
    return service.list_rules(
        page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
    )


@router.post("/category-rules", response_model=CategoryRuleOut, status_code=201)
def create_rule(data: CategoryRuleCreate, db: Session = Depends(get_db)):
    service = CategoryRuleService(db)
    return service.create_rule(data)
