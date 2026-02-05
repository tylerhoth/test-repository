from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.dashboard import (
    CategorySpending,
    DashboardSummary,
    IncomeVsExpensesResponse,
    MonthlyComparison,
    RecurringCharge,
    RecurringChargesResponse,
    SpendingByCategoryResponse,
)


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_summary(self) -> DashboardSummary:
        result = self.db.execute(
            select(
                func.coalesce(
                    func.sum(
                        case((Transaction.amount > 0, Transaction.amount), else_=0)
                    ),
                    0,
                ).label("income_cents"),
                func.coalesce(
                    func.sum(
                        case(
                            (Transaction.amount < 0, func.abs(Transaction.amount)),
                            else_=0,
                        )
                    ),
                    0,
                ).label("expenses_cents"),
                func.count().label("txn_count"),
            )
        ).one()

        income_cents = result.income_cents
        expenses_cents = result.expenses_cents

        income = income_cents / 100
        expenses = expenses_cents / 100
        net = income - expenses
        savings_rate = (net / income * 100) if income > 0 else 0.0

        account_count = (
            self.db.execute(select(func.count()).select_from(Account)).scalar() or 0
        )

        return DashboardSummary(
            total_income=round(income, 2),
            total_expenses=round(expenses, 2),
            net_savings=round(net, 2),
            savings_rate=round(savings_rate, 1),
            transaction_count=result.txn_count,
            account_count=account_count,
        )

    def spending_by_category(self) -> SpendingByCategoryResponse:
        rows = self.db.execute(
            select(
                Transaction.category_id,
                func.coalesce(Category.name, "Uncategorized").label("category_name"),
                func.sum(func.abs(Transaction.amount)).label("total_cents"),
                func.count().label("txn_count"),
            )
            .outerjoin(Category, Transaction.category_id == Category.id)
            .where(Transaction.amount < 0)
            .group_by(Transaction.category_id, Category.name)
            .order_by(func.sum(func.abs(Transaction.amount)).desc())
        ).all()

        total_expenses_cents = sum(r.total_cents for r in rows)
        total_expenses = total_expenses_cents / 100

        items = [
            CategorySpending(
                category_id=r.category_id,
                category_name=r.category_name,
                total=round(r.total_cents / 100, 2),
                transaction_count=r.txn_count,
                percentage=(
                    round(r.total_cents / total_expenses_cents * 100, 1)
                    if total_expenses_cents > 0
                    else 0
                ),
            )
            for r in rows
        ]

        return SpendingByCategoryResponse(
            items=items, total_expenses=round(total_expenses, 2)
        )

    def income_vs_expenses(self) -> IncomeVsExpensesResponse:
        rows = self.db.execute(
            select(
                func.strftime("%Y-%m", Transaction.date).label("month"),
                func.coalesce(
                    func.sum(
                        case((Transaction.amount > 0, Transaction.amount), else_=0)
                    ),
                    0,
                ).label("income_cents"),
                func.coalesce(
                    func.sum(
                        case(
                            (Transaction.amount < 0, func.abs(Transaction.amount)),
                            else_=0,
                        )
                    ),
                    0,
                ).label("expenses_cents"),
            )
            .group_by(func.strftime("%Y-%m", Transaction.date))
            .order_by(func.strftime("%Y-%m", Transaction.date))
        ).all()

        items = [
            MonthlyComparison(
                month=r.month,
                income=round(r.income_cents / 100, 2),
                expenses=round(r.expenses_cents / 100, 2),
                net=round((r.income_cents - r.expenses_cents) / 100, 2),
            )
            for r in rows
        ]

        return IncomeVsExpensesResponse(items=items)

    def recurring_charges(self) -> RecurringChargesResponse:
        """Detect recurring charges by finding descriptions that appear 3+ times."""
        rows = self.db.execute(
            select(
                Transaction.description,
                func.avg(func.abs(Transaction.amount)).label("avg_cents"),
                func.count().label("occurrences"),
                Transaction.category_id,
            )
            .where(Transaction.amount < 0)
            .group_by(Transaction.description)
            .having(func.count() >= 3)
            .order_by(func.count().desc())
            .limit(50)
        ).all()

        # Look up category names for grouped results
        cat_ids = {r.category_id for r in rows if r.category_id is not None}
        cat_names: dict[int, str] = {}
        if cat_ids:
            cats = self.db.execute(
                select(Category.id, Category.name).where(Category.id.in_(cat_ids))
            ).all()
            cat_names = {c.id: c.name for c in cats}

        items = []
        total_monthly = 0.0
        for r in rows:
            avg = round(r.avg_cents / 100, 2)
            occurrences = r.occurrences

            if occurrences >= 60:
                freq = "daily"
                monthly_est = avg * 30
            elif occurrences >= 8:
                freq = "biweekly"
                monthly_est = avg * 2
            elif occurrences >= 3:
                freq = "monthly"
                monthly_est = avg
            else:
                freq = "occasional"
                monthly_est = avg

            total_monthly += monthly_est
            items.append(
                RecurringCharge(
                    description=r.description,
                    average_amount=avg,
                    frequency=freq,
                    occurrences=occurrences,
                    category_name=(
                        cat_names.get(r.category_id) if r.category_id else None
                    ),
                )
            )

        return RecurringChargesResponse(
            items=items,
            total_monthly_recurring=round(total_monthly, 2),
        )
