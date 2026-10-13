"""
Database Connection & Engine Initialization Module.
Provides SQLAlchemy Base, engine, and connection health check helpers.
"""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base

from backend.app.core.config import settings

logger = logging.getLogger("medicine.backend.db")

# Create Declarative Base for ORM Models
Base = declarative_base()

# Configure SQLAlchemy Engine
db_url = settings.database_url

# Configure pooling parameters based on DB type
connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        echo=False
    )
else:
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        echo=False
    )


def check_db_connection() -> bool:
    """
    Verifies database connectivity.
    Returns True if connection succeeds, False otherwise.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.warning(f"Database connection check failed: {e}")
        return False


def init_db():
    """
    Creates tables for all registered ORM models if database is reachable.
    """
    try:
        # Import models so they are registered with Base metadata
        from backend.app.models import PlantModel, MedicineModel, HistoryModel  # noqa: F401
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database schemas verified/created successfully.")
    except Exception as e:
        logger.warning(f"Database initialization deferred (database not reachable yet): {e}")
