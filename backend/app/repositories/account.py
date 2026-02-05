from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.account import Account

SORTABLE_FIELDS = {"id", "name", "institution", "account_type", "created_at"}


class AccountRepository:
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
    ) -> tuple[list[Account], int]:
        query = select(Account)
        count_query = select(func.count()).select_from(Account)

        if q:
            query = query.where(Account.name.ilike(f"%{q}%"))
            count_query = count_query.where(Account.name.ilike(f"%{q}%"))

        if sort_by in SORTABLE_FIELDS:
            col = getattr(Account, sort_by)
            query = query.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = self.db.execute(count_query).scalar() or 0
        offset = (page - 1) * page_size
        items = list(self.db.execute(query.offset(offset).limit(page_size)).scalars().all())
        return items, total

    def create(
        self, *, name: str, institution: str, account_type: str, last_four: str | None = None
    ) -> Account:
        account = Account(
            name=name, institution=institution, account_type=account_type, last_four=last_four
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_by_id(self, account_id: int) -> Account | None:
        return self.db.get(Account, account_id)

    def find_by_name_and_institution(self, name: str, institution: str) -> Account | None:
        return self.db.execute(
            select(Account).where(Account.name == name, Account.institution == institution)
        ).scalar_one_or_none()
