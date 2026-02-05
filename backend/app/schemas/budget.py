from datetime import datetime

from pydantic import BaseModel


class BudgetCreate(BaseModel):
    category_id: int
    amount_limit: float


class BudgetOut(BaseModel):
    id: int
    category_id: int
    amount_limit: float
    created_at: datetime

    model_config = {"from_attributes": True}


class BudgetListResponse(BaseModel):
    items: list[BudgetOut]
    total: int
    page: int
    page_size: int
