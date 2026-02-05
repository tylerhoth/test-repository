from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, func

from app.models.base import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, unique=True)
    amount_limit = Column(Float, nullable=False)  # monthly budget limit
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
