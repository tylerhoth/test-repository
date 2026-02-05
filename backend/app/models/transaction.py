from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, func

from app.models.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    raw_description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)  # negative = expense, positive = income
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    is_recurring = Column(Boolean, default=False, nullable=False)
    tags = Column(String, nullable=True)  # comma-separated
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
