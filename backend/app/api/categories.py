from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schemas.category import CategoryCreate, CategoryListResponse, CategoryOut
from app.services.category import CategoryService

router = APIRouter()


@router.get("/categories", response_model=CategoryListResponse)
def list_categories(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=200),
    q: str | None = Query(None),
    sort_by: str = Query("name"),
    sort_dir: Literal["asc", "desc"] = Query("asc"),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)
    return service.list_categories(
        page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
    )


@router.post("/categories", response_model=CategoryOut, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create_category(data)
