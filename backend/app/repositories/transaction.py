from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction

SORTABLE_FIELDS = {"id", "date", "description", "amount", "created_at"}


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        sort_by: str = "date",
        sort_dir: str = "desc",
        account_id: int | None = None,
        category_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> tuple[list[Transaction], int]:
        query = select(Transaction)
        count_query = select(func.count()).select_from(Transaction)

        if q:
            query = query.where(Transaction.description.ilike(f"%{q}%"))
            count_query = count_query.where(Transaction.description.ilike(f"%{q}%"))

        if account_id is not None:
            query = query.where(Transaction.account_id == account_id)
            count_query = count_query.where(Transaction.account_id == account_id)

        if category_id is not None:
            query = query.where(Transaction.category_id == category_id)
            count_query = count_query.where(Transaction.category_id == category_id)

        if date_from is not None:
            query = query.where(Transaction.date >= date_from)
            count_query = count_query.where(Transaction.date >= date_from)

        if date_to is not None:
            query = query.where(Transaction.date <= date_to)
            count_query = count_query.where(Transaction.date <= date_to)

        if sort_by in SORTABLE_FIELDS:
            col = getattr(Transaction, sort_by)
            query = query.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = self.db.execute(count_query).scalar() or 0
        offset = (page - 1) * page_size
        items = list(self.db.execute(query.offset(offset).limit(page_size)).scalars().all())
        return items, total

    def create(self, **kwargs) -> Transaction:
        txn = Transaction(**kwargs)
        self.db.add(txn)
        self.db.commit()
        self.db.refresh(txn)
        return txn

    def bulk_create(self, transactions: list[dict]) -> list[Transaction]:
        objs = [Transaction(**t) for t in transactions]
        self.db.add_all(objs)
        self.db.commit()
        for obj in objs:
            self.db.refresh(obj)
        return objs

    def get_by_id(self, txn_id: int) -> Transaction | None:
        return self.db.get(Transaction, txn_id)

    def update(self, txn_id: int, **kwargs) -> Transaction | None:
        txn = self.get_by_id(txn_id)
        if not txn:
            return None
        for key, value in kwargs.items():
            setattr(txn, key, value)
        self.db.commit()
        self.db.refresh(txn)
        return txn

    def delete(self, txn_id: int) -> bool:
        txn = self.get_by_id(txn_id)
        if not txn:
            return False
        self.db.delete(txn)
        self.db.commit()
        return True
