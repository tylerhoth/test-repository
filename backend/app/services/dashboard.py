from collections import Counter, defaultdict

from sqlalchemy import func, select
from sqlalchemy.orm import Session

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
        rows = list(self.db.execute(select(Transaction.amount)).scalars().all())
        income = sum(a for a in rows if a > 0)
        expenses = abs(sum(a for a in rows if a < 0))
        net = income - expenses
        savings_rate = (net / income * 100) if income > 0 else 0.0

        from app.models.account import Account

        account_count = self.db.execute(select(func.count()).select_from(Account)).scalar() or 0

        return DashboardSummary(
            total_income=round(income, 2),
            total_expenses=round(expenses, 2),
            net_savings=round(net, 2),
            savings_rate=round(savings_rate, 1),
            transaction_count=len(rows),
            account_count=account_count,
        )

    def spending_by_category(self) -> SpendingByCategoryResponse:
        # Only expenses (negative amounts)
        rows = list(
            self.db.execute(
                select(Transaction.category_id, Transaction.amount).where(Transaction.amount < 0)
            ).all()
        )

        # Group by category
        cat_totals: dict[int | None, float] = defaultdict(float)
        cat_counts: dict[int | None, int] = Counter()
        for cat_id, amount in rows:
            cat_totals[cat_id] += abs(amount)
            cat_counts[cat_id] += 1

        total_expenses = sum(cat_totals.values())

        # Look up category names
        cat_names: dict[int | None, str] = {None: "Uncategorized"}
        cat_ids = [cid for cid in cat_totals if cid is not None]
        if cat_ids:
            cats = list(
                self.db.execute(
                    select(Category.id, Category.name).where(Category.id.in_(cat_ids))
                ).all()
            )
            for cid, cname in cats:
                cat_names[cid] = cname

        items = []
        for cat_id, total in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
            items.append(
                CategorySpending(
                    category_id=cat_id,
                    category_name=cat_names.get(cat_id, "Unknown"),
                    total=round(total, 2),
                    transaction_count=cat_counts[cat_id],
                    percentage=round(total / total_expenses * 100, 1) if total_expenses > 0 else 0,
                )
            )

        return SpendingByCategoryResponse(items=items, total_expenses=round(total_expenses, 2))

    def income_vs_expenses(self) -> IncomeVsExpensesResponse:
        rows = list(self.db.execute(select(Transaction.date, Transaction.amount)).all())

        monthly: dict[str, dict[str, float]] = defaultdict(lambda: {"income": 0.0, "expenses": 0.0})
        for txn_date, amount in rows:
            month_key = txn_date.strftime("%Y-%m")
            if amount > 0:
                monthly[month_key]["income"] += amount
            else:
                monthly[month_key]["expenses"] += abs(amount)

        items = []
        for month in sorted(monthly.keys()):
            data = monthly[month]
            items.append(
                MonthlyComparison(
                    month=month,
                    income=round(data["income"], 2),
                    expenses=round(data["expenses"], 2),
                    net=round(data["income"] - data["expenses"], 2),
                )
            )

        return IncomeVsExpensesResponse(items=items)

    def recurring_charges(self) -> RecurringChargesResponse:
        """Detect recurring charges by finding descriptions that appear 3+ times."""
        rows = list(
            self.db.execute(
                select(Transaction.description, Transaction.amount, Transaction.category_id).where(
                    Transaction.amount < 0
                )
            ).all()
        )

        # Group by description
        desc_data: dict[str, list[float]] = defaultdict(list)
        desc_cats: dict[str, int | None] = {}
        for desc, amount, cat_id in rows:
            desc_data[desc].append(abs(amount))
            desc_cats[desc] = cat_id

        # Get category names
        all_cat_ids = {cid for cid in desc_cats.values() if cid is not None}
        cat_names: dict[int | None, str] = {}
        if all_cat_ids:
            cats = list(
                self.db.execute(
                    select(Category.id, Category.name).where(Category.id.in_(all_cat_ids))
                ).all()
            )
            cat_names = {cid: cname for cid, cname in cats}

        items = []
        total_monthly = 0.0
        for desc, amounts in sorted(desc_data.items(), key=lambda x: len(x[1]), reverse=True):
            if len(amounts) < 3:
                continue
            avg = sum(amounts) / len(amounts)
            occurrences = len(amounts)

            # Estimate frequency
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
            cat_id = desc_cats.get(desc)
            items.append(
                RecurringCharge(
                    description=desc,
                    average_amount=round(avg, 2),
                    frequency=freq,
                    occurrences=occurrences,
                    category_name=cat_names.get(cat_id) if cat_id else None,
                )
            )

        return RecurringChargesResponse(
            items=items[:50],  # Top 50 recurring
            total_monthly_recurring=round(total_monthly, 2),
        )
