from sqlalchemy.orm import Session

from app.repositories.account import AccountRepository
from app.schemas.account import AccountCreate, AccountListResponse, AccountOut


class AccountService:
    def __init__(self, db: Session):
        self.repo = AccountRepository(db)

    def list_accounts(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        sort_by: str = "id",
        sort_dir: str = "asc",
    ) -> AccountListResponse:
        items, total = self.repo.list(
            page=page, page_size=page_size, q=q, sort_by=sort_by, sort_dir=sort_dir
        )
        return AccountListResponse(
            items=[AccountOut.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    def create_account(self, data: AccountCreate) -> AccountOut:
        account = self.repo.create(
            name=data.name,
            institution=data.institution,
            account_type=data.account_type,
            last_four=data.last_four,
        )
        return AccountOut.model_validate(account)
