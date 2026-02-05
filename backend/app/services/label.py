from sqlalchemy.orm import Session

from app.repositories.label import LabelRepository
from app.schemas.label import LabelCreate, LabelListResponse, LabelOut


class LabelService:
    def __init__(self, db: Session):
        self.repo = LabelRepository(db)

    def list_labels(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        sort_by: str = "name",
        sort_dir: str = "asc",
    ) -> LabelListResponse:
        items, total = self.repo.list(
            page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
        )
        return LabelListResponse(
            items=[LabelOut.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    def create_label(self, data: LabelCreate) -> LabelOut:
        label = self.repo.create(name=data.name, color=data.color)
        return LabelOut.model_validate(label)

    def delete_label(self, label_id: int) -> bool:
        return self.repo.delete(label_id)
