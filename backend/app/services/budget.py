from sqlalchemy.orm import Session

from app.repositories.budget import BudgetRepository
from app.schemas.budget import BudgetCreate, BudgetListResponse, BudgetOut


class BudgetService:
    def __init__(self, db: Session):
        self.repo = BudgetRepository(db)

    def list_budgets(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "id",
        sort_dir: str = "asc",
    ) -> BudgetListResponse:
        items, total = self.repo.list(
            page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir
        )
        return BudgetListResponse(
            items=[BudgetOut.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    def create_or_update_budget(self, data: BudgetCreate) -> BudgetOut:
        budget = self.repo.create_or_update(
            category_id=data.category_id,
            amount_limit=int(round(data.amount_limit * 100)),
        )
        return BudgetOut.model_validate(budget)

    def delete_budget(self, budget_id: int) -> bool:
        return self.repo.delete(budget_id)
