from datetime import datetime

from pydantic import BaseModel, field_validator


class BudgetCreate(BaseModel):
    category_id: int
    amount_limit: float  # dollars; converted to integer cents in service layer


class BudgetOut(BaseModel):
    id: int
    category_id: int
    amount_limit: float
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("amount_limit", mode="before")
    @classmethod
    def cents_to_dollars(cls, v: object) -> object:
        """DB stores integer cents; convert to dollars for API output."""
        if isinstance(v, int):
            return v / 100
        return v


class BudgetListResponse(BaseModel):
    items: list[BudgetOut]
    total: int
    page: int
    page_size: int
