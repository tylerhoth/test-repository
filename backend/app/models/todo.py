from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.models.base import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
