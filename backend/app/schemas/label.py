from datetime import datetime

from pydantic import BaseModel


class LabelCreate(BaseModel):
    name: str
    color: str = "#6B7280"


class LabelOut(BaseModel):
    id: int
    name: str
    color: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LabelListResponse(BaseModel):
    items: list[LabelOut]
    total: int
    page: int
    page_size: int
