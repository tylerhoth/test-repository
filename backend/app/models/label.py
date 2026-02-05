from sqlalchemy import Column, DateTime, Integer, String, func

from app.models.base import Base


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=False, default="#6B7280")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
