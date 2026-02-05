from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.budget import Budget

SORTABLE_FIELDS = {"id", "amount_limit", "created_at"}


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "id",
        sort_dir: str = "asc",
    ) -> tuple[list[Budget], int]:
        query = select(Budget)
        count_query = select(func.count()).select_from(Budget)

        if sort_by in SORTABLE_FIELDS:
            col = getattr(Budget, sort_by)
            query = query.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = self.db.execute(count_query).scalar() or 0
        offset = (page - 1) * page_size
        items = list(self.db.execute(query.offset(offset).limit(page_size)).scalars().all())
        return items, total

    def create_or_update(self, *, category_id: int, amount_limit: float) -> Budget:
        existing = self.db.execute(
            select(Budget).where(Budget.category_id == category_id)
        ).scalar_one_or_none()
        if existing:
            existing.amount_limit = amount_limit
            self.db.commit()
            self.db.refresh(existing)
            return existing
        budget = Budget(category_id=category_id, amount_limit=amount_limit)
        self.db.add(budget)
        self.db.commit()
        self.db.refresh(budget)
        return budget

    def get_by_id(self, budget_id: int) -> Budget | None:
        return self.db.get(Budget, budget_id)

    def delete(self, budget_id: int) -> bool:
        budget = self.get_by_id(budget_id)
        if not budget:
            return False
        self.db.delete(budget)
        self.db.commit()
        return True
