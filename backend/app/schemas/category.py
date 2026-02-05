from datetime import datetime

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    is_system: bool = False


class CategoryOut(BaseModel):
    id: int
    name: str
    is_system: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class CategoryListResponse(BaseModel):
    items: list[CategoryOut]
    total: int
    page: int
    page_size: int
