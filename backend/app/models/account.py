from sqlalchemy import Column, DateTime, Integer, String, func

from app.models.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    account_type = Column(
        String, nullable=False
    )  # checking, credit_card, savings, ira, 401k, mortgage, loan, brokerage
    last_four = Column(String(4), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
