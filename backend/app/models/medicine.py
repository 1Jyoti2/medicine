"""
Pharmaceutical Medicine ORM Model.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON
from backend.app.db.database import Base


class MedicineModel(Base):
    __tablename__ = "pharmaceutical_medicines"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(150), unique=True, index=True, nullable=False)
    generic_name = Column(String(150), index=True, nullable=False)
    category = Column(String(100), nullable=True)
    composition = Column(String(200), nullable=True)
    manufacturer = Column(String(150), nullable=True)
    dosage = Column(String(50), nullable=True)
    storage = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    uses = Column(JSON, nullable=True)
    side_effects = Column(JSON, nullable=True)
    precautions = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
