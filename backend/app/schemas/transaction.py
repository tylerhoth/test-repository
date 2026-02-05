from datetime import date, datetime

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    date: date
    description: str
    amount: float
    category_id: int | None = None
    account_id: int | None = None
    tags: str | None = None
    notes: str | None = None


class TransactionUpdate(BaseModel):
    category_id: int | None = None
    tags: str | None = None
    notes: str | None = None
    is_recurring: bool | None = None


class TransactionOut(BaseModel):
    id: int
    date: date
    description: str
    raw_description: str | None
    amount: float
    category_id: int | None
    account_id: int | None
    is_recurring: bool
    tags: str | None
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    items: list[TransactionOut]
    total: int
    page: int
    page_size: int


class ImportResult(BaseModel):
    imported: int
    skipped: int
    accounts_created: int
    categories_created: int
