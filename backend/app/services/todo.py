from sqlalchemy.orm import Session

from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoListResponse, TodoOut


class TodoService:
    def __init__(self, db: Session):
        self.repo = TodoRepository(db)

    def list_todos(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        sort_by: str = "id",
        sort_dir: str = "asc",
    ) -> TodoListResponse:
        items, total = self.repo.list(
            page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
        )
        return TodoListResponse(
            items=[TodoOut.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    def create_todo(self, data: TodoCreate) -> TodoOut:
        todo = self.repo.create(title=data.title, completed=data.completed)
        return TodoOut.model_validate(todo)

    def delete_todo(self, todo_id: int) -> bool:
        return self.repo.delete(todo_id)
