from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryListResponse, CategoryOut


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def list_categories(
        self,
        *,
        page: int = 1,
        page_size: int = 100,
        q: str | None = None,
        sort_by: str = "name",
        sort_dir: str = "asc",
    ) -> CategoryListResponse:
        items, total = self.repo.list(
            page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
        )
        return CategoryListResponse(
            items=[CategoryOut.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    def create_category(self, data: CategoryCreate) -> CategoryOut:
        category = self.repo.create(name=data.name, is_system=data.is_system)
        return CategoryOut.model_validate(category)
