from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.todo import Todo

SORTABLE_FIELDS = {"id", "title", "completed", "created_at"}


class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        sort_by: str = "id",
        sort_dir: str = "asc",
    ) -> tuple[list[Todo], int]:
        query = select(Todo)
        count_query = select(func.count()).select_from(Todo)

        if q:
            query = query.where(Todo.title.ilike(f"%{q}%"))
            count_query = count_query.where(Todo.title.ilike(f"%{q}%"))

        if sort_by in SORTABLE_FIELDS:
            col = getattr(Todo, sort_by)
            query = query.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = self.db.execute(count_query).scalar() or 0
        offset = (page - 1) * page_size
        items = list(self.db.execute(query.offset(offset).limit(page_size)).scalars().all())
        return items, total

    def create(self, *, title: str, completed: bool = False) -> Todo:
        todo = Todo(title=title, completed=completed)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def get_by_id(self, todo_id: int) -> Todo | None:
        return self.db.get(Todo, todo_id)

    def delete(self, todo_id: int) -> bool:
        todo = self.get_by_id(todo_id)
        if not todo:
            return False
        self.db.delete(todo)
        self.db.commit()
        return True
