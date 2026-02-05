from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schemas.todo import TodoCreate, TodoListResponse, TodoOut
from app.services.todo import TodoService

router = APIRouter()


@router.get("/todos", response_model=TodoListResponse)
def list_todos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None),
    sort_by: str = Query("id"),
    sort_dir: Literal["asc", "desc"] = Query("asc"),
    db: Session = Depends(get_db),
):
    service = TodoService(db)
    return service.list_todos(
        page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
    )


@router.post("/todos", response_model=TodoOut, status_code=201)
def create_todo(data: TodoCreate, db: Session = Depends(get_db)):
    service = TodoService(db)
    return service.create_todo(data)


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    service = TodoService(db)
    deleted = service.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
