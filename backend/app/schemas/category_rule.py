from datetime import datetime

from pydantic import BaseModel


class CategoryRuleCreate(BaseModel):
    pattern: str
    category_id: int
    confidence: float = 1.0


class CategoryRuleOut(BaseModel):
    id: int
    pattern: str
    category_id: int
    confidence: float
    times_applied: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CategoryRuleListResponse(BaseModel):
    items: list[CategoryRuleOut]
    total: int
    page: int
    page_size: int
