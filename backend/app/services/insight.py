from sqlalchemy.orm import Session

from app.repositories.insight import InsightRepository
from app.schemas.insight import InsightListResponse, InsightOut


class InsightService:
    def __init__(self, db: Session):
        self.repo = InsightRepository(db)

    def list_insights(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
    ) -> InsightListResponse:
        items, total = self.repo.list(
            page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir
        )
        return InsightListResponse(
            items=[InsightOut.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )
