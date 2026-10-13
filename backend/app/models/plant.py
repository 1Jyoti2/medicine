"""
Plant ORM Model.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from backend.app.db.database import Base


class PlantModel(Base):
    __tablename__ = "medicinal_plants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    scientific_name = Column(String(150), index=True, nullable=False)
    family = Column(String(100), nullable=True)
    native_region = Column(String(200), nullable=True)
    image_url = Column(String(255), nullable=True)
    parts_used = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    uses = Column(JSON, nullable=True)
    active_compounds = Column(JSON, nullable=True)
    precautions = Column(JSON, nullable=True)
    side_effects = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
