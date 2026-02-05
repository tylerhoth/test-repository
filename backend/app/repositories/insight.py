from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.insight import Insight

SORTABLE_FIELDS = {"id", "insight_type", "severity", "created_at"}


class InsightRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
    ) -> tuple[list[Insight], int]:
        query = select(Insight)
        count_query = select(func.count()).select_from(Insight)

        if sort_by in SORTABLE_FIELDS:
            col = getattr(Insight, sort_by)
            query = query.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = self.db.execute(count_query).scalar() or 0
        offset = (page - 1) * page_size
        items = list(self.db.execute(query.offset(offset).limit(page_size)).scalars().all())
        return items, total

    def create(self, **kwargs) -> Insight:
        insight = Insight(**kwargs)
        self.db.add(insight)
        self.db.commit()
        self.db.refresh(insight)
        return insight

    def clear_all(self) -> int:
        count = self.db.execute(select(func.count()).select_from(Insight)).scalar() or 0
        self.db.query(Insight).delete()
        self.db.commit()
        return count
