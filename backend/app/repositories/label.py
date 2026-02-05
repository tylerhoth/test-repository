from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.label import Label

SORTABLE_FIELDS = {"id", "name", "created_at"}


class LabelRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        sort_by: str = "name",
        sort_dir: str = "asc",
    ) -> tuple[list[Label], int]:
        query = select(Label)
        count_query = select(func.count()).select_from(Label)

        if q:
            query = query.where(Label.name.ilike(f"%{q}%"))
            count_query = count_query.where(Label.name.ilike(f"%{q}%"))

        if sort_by in SORTABLE_FIELDS:
            col = getattr(Label, sort_by)
            query = query.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = self.db.execute(count_query).scalar() or 0
        offset = (page - 1) * page_size
        items = list(self.db.execute(query.offset(offset).limit(page_size)).scalars().all())
        return items, total

    def create(self, *, name: str, color: str = "#6B7280") -> Label:
        label = Label(name=name, color=color)
        self.db.add(label)
        self.db.commit()
        self.db.refresh(label)
        return label

    def get_by_id(self, label_id: int) -> Label | None:
        return self.db.get(Label, label_id)

    def delete(self, label_id: int) -> bool:
        label = self.get_by_id(label_id)
        if not label:
            return False
        self.db.delete(label)
        self.db.commit()
        return True
