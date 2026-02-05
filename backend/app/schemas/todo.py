from datetime import datetime

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    completed: bool = False


class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TodoListResponse(BaseModel):
    items: list[TodoOut]
    total: int
    page: int
    page_size: int
