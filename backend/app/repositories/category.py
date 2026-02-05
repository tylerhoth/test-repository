from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.category import Category

SORTABLE_FIELDS = {"id", "name", "created_at"}


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 100,
        q: str | None = None,
        sort_by: str = "name",
        sort_dir: str = "asc",
    ) -> tuple[list[Category], int]:
        query = select(Category)
        count_query = select(func.count()).select_from(Category)

        if q:
            query = query.where(Category.name.ilike(f"%{q}%"))
            count_query = count_query.where(Category.name.ilike(f"%{q}%"))

        if sort_by in SORTABLE_FIELDS:
            col = getattr(Category, sort_by)
            query = query.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = self.db.execute(count_query).scalar() or 0
        offset = (page - 1) * page_size
        items = list(self.db.execute(query.offset(offset).limit(page_size)).scalars().all())
        return items, total

    def create(self, *, name: str, is_system: bool = False) -> Category:
        category = Category(name=name, is_system=is_system)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_by_id(self, category_id: int) -> Category | None:
        return self.db.get(Category, category_id)

    def find_by_name(self, name: str) -> Category | None:
        return self.db.execute(select(Category).where(Category.name == name)).scalar_one_or_none()

    def get_or_create(self, name: str, is_system: bool = True) -> Category:
        existing = self.find_by_name(name)
        if existing:
            return existing
        return self.create(name=name, is_system=is_system)
