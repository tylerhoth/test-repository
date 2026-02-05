from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate: float  # percentage
    transaction_count: int
    account_count: int


class CategorySpending(BaseModel):
    category_id: int | None
    category_name: str
    total: float
    transaction_count: int
    percentage: float  # of total expenses


class SpendingByCategoryResponse(BaseModel):
    items: list[CategorySpending]
    total_expenses: float


class MonthlyComparison(BaseModel):
    month: str  # YYYY-MM
    income: float
    expenses: float
    net: float


class IncomeVsExpensesResponse(BaseModel):
    items: list[MonthlyComparison]


class RecurringCharge(BaseModel):
    description: str
    average_amount: float
    frequency: str
    occurrences: int
    category_name: str | None


class RecurringChargesResponse(BaseModel):
    items: list[RecurringCharge]
    total_monthly_recurring: float
