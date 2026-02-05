from datetime import datetime

from pydantic import BaseModel


class AccountCreate(BaseModel):
    name: str
    institution: str
    account_type: str
    last_four: str | None = None


class AccountOut(BaseModel):
    id: int
    name: str
    institution: str
    account_type: str
    last_four: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AccountListResponse(BaseModel):
    items: list[AccountOut]
    total: int
    page: int
    page_size: int
