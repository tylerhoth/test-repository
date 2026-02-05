from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, func

from app.models.base import Base


class RecurrenceGroup(Base):
    __tablename__ = "recurrence_groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description_pattern = Column(String, nullable=False)
    expected_amount = Column(Integer, nullable=False)  # cents
    frequency = Column(
        String, nullable=False
    )  # daily, weekly, biweekly, monthly, quarterly, annual
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_seen = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
