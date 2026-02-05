from datetime import datetime

from pydantic import BaseModel


class InsightOut(BaseModel):
    id: int
    insight_type: str
    title: str
    description: str
    severity: str
    data_json: str | None
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class InsightListResponse(BaseModel):
    items: list[InsightOut]
    total: int
    page: int
    page_size: int
