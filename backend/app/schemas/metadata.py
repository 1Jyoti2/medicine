"""
Metadata & History Schemas.
"""

from typing import List, Optional, Any
from pydantic import BaseModel


class HistoryItem(BaseModel):
    id: str
    name: str
    type: str
    confidence: float
    date: str
    status: str
    resultId: str


class HealthStatus(BaseModel):
    status: str
    timestamp: float
    services: dict
