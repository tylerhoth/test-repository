from sqlalchemy import Column, DateTime, ForeignKey, Integer, func

from app.models.base import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, unique=True)
    amount_limit = Column(Integer, nullable=False)  # cents; monthly budget limit
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
