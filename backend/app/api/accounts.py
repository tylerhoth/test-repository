from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schemas.account import AccountCreate, AccountListResponse, AccountOut
from app.services.account import AccountService

router = APIRouter()


@router.get("/accounts", response_model=AccountListResponse)
def list_accounts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort_by: str = Query("id"),
    sort_dir: Literal["asc", "desc"] = Query("asc"),
    db: Session = Depends(get_db),
):
    service = AccountService(db)
    return service.list_accounts(
        page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
    )


@router.post("/accounts", response_model=AccountOut, status_code=201)
def create_account(data: AccountCreate, db: Session = Depends(get_db)):
    service = AccountService(db)
    return service.create_account(data)
