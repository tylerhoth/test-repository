from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schemas.transaction import (
    ImportResult,
    TransactionCreate,
    TransactionListResponse,
    TransactionOut,
    TransactionUpdate,
)
from app.services.transaction import TransactionService

router = APIRouter()


@router.get("/transactions", response_model=TransactionListResponse)
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort_by: str = Query("date"),
    sort_dir: Literal["asc", "desc"] = Query("desc"),
    account_id: int | None = Query(None),
    category_id: int | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    db: Session = Depends(get_db),
):
    service = TransactionService(db)
    return service.list_transactions(
        page=page,
        page_size=page_size,
        q=q,
        sort_by=sort_by,
        sort_dir=sort_dir,
        account_id=account_id,
        category_id=category_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.post("/transactions", response_model=TransactionOut, status_code=201)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.create_transaction(data)


@router.put("/transactions/{txn_id}", response_model=TransactionOut)
def update_transaction(txn_id: int, data: TransactionUpdate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    result = service.update_transaction(txn_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result


@router.delete("/transactions/{txn_id}", status_code=204)
def delete_transaction(txn_id: int, db: Session = Depends(get_db)):
    service = TransactionService(db)
    deleted = service.delete_transaction(txn_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")


@router.post("/transactions/import", response_model=ImportResult)
async def import_transactions(file: UploadFile, db: Session = Depends(get_db)):
    content = await file.read()
    csv_text = content.decode("utf-8")

    # Strip optional header line like "Transactions For All Accounts..."
    lines = csv_text.split("\n")
    if lines and not lines[0].startswith("Date") and "Date" not in lines[0].split(",")[0]:
        csv_text = "\n".join(lines[1:])

    service = TransactionService(db)
    return service.import_csv(csv_text)
