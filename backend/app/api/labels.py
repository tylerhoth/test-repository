from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schemas.label import LabelCreate, LabelListResponse, LabelOut
from app.services.label import LabelService

router = APIRouter()


@router.get("/labels", response_model=LabelListResponse)
def list_labels(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort_by: str = Query("name"),
    sort_dir: Literal["asc", "desc"] = Query("asc"),
    db: Session = Depends(get_db),
):
    service = LabelService(db)
    return service.list_labels(
        page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
    )


@router.post("/labels", response_model=LabelOut, status_code=201)
def create_label(data: LabelCreate, db: Session = Depends(get_db)):
    service = LabelService(db)
    return service.create_label(data)


@router.delete("/labels/{label_id}", status_code=204)
def delete_label(label_id: int, db: Session = Depends(get_db)):
    service = LabelService(db)
    deleted = service.delete_label(label_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Label not found")
