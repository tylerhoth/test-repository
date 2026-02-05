from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schemas.insight import InsightListResponse
from app.services.insight import InsightService

router = APIRouter()


@router.get("/insights", response_model=InsightListResponse)
def list_insights(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_dir: Literal["asc", "desc"] = Query("desc"),
    db: Session = Depends(get_db),
):
    service = InsightService(db)
    return service.list_insights(page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir)
