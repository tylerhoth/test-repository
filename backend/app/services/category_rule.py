from sqlalchemy.orm import Session

from app.repositories.category_rule import CategoryRuleRepository
from app.schemas.category_rule import CategoryRuleCreate, CategoryRuleListResponse, CategoryRuleOut


class CategoryRuleService:
    def __init__(self, db: Session):
        self.repo = CategoryRuleRepository(db)

    def list_rules(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        sort_by: str = "id",
        sort_dir: str = "asc",
    ) -> CategoryRuleListResponse:
        items, total = self.repo.list(
            page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
        )
        return CategoryRuleListResponse(
            items=[CategoryRuleOut.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    def create_rule(self, data: CategoryRuleCreate) -> CategoryRuleOut:
        rule = self.repo.create(
            pattern=data.pattern,
            category_id=data.category_id,
            confidence=data.confidence,
        )
        return CategoryRuleOut.model_validate(rule)
