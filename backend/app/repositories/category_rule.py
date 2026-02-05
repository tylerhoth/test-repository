from sqlalchemy import func, literal, select
from sqlalchemy.orm import Session

from app.models.category_rule import CategoryRule

SORTABLE_FIELDS = {"id", "pattern", "confidence", "times_applied", "created_at"}


class CategoryRuleRepository:
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
    ) -> tuple[list[CategoryRule], int]:
        query = select(CategoryRule)
        count_query = select(func.count()).select_from(CategoryRule)

        if q:
            query = query.where(CategoryRule.pattern.ilike(f"%{q}%"))
            count_query = count_query.where(CategoryRule.pattern.ilike(f"%{q}%"))

        if sort_by in SORTABLE_FIELDS:
            col = getattr(CategoryRule, sort_by)
            query = query.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = self.db.execute(count_query).scalar() or 0
        offset = (page - 1) * page_size
        items = list(self.db.execute(query.offset(offset).limit(page_size)).scalars().all())
        return items, total

    def create(self, *, pattern: str, category_id: int, confidence: float = 1.0) -> CategoryRule:
        rule = CategoryRule(pattern=pattern, category_id=category_id, confidence=confidence)
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def find_matching(self, description: str) -> CategoryRule | None:
        """Find the best matching rule for a description using a DB query."""
        desc_lower = description.lower()
        return self.db.execute(
            select(CategoryRule)
            .where(literal(desc_lower).contains(func.lower(CategoryRule.pattern)))
            .order_by(CategoryRule.confidence.desc())
            .limit(1)
        ).scalar_one_or_none()

    def increment_applied(self, rule_id: int) -> None:
        rule = self.db.get(CategoryRule, rule_id)
        if rule:
            rule.times_applied += 1
            self.db.commit()
