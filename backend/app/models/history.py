"""
Scan & Prediction Detection History ORM Model.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.app.db.database import Base


class HistoryModel(Base):
    __tablename__ = "detection_history"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    type = Column(String(50), nullable=False)  # 'Medicinal Leaf', 'Prescription', 'Tablet'
    confidence = Column(Float, nullable=False)
    date = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    result_id = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
