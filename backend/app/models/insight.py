from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.models.base import Base


class Insight(Base):
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    insight_type = Column(
        String, nullable=False
    )  # anomaly, trend, saving_opportunity, recurring_detected
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    severity = Column(String, default="info", nullable=False)  # info, warning, alert
    data_json = Column(String, nullable=True)  # JSON blob for supplementary data
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
