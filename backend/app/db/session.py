"""
Database Session Management Module.
Provides sessionmaker and FastAPI dependency generator get_db().
"""

import logging
from typing import Generator
from sqlalchemy.orm import sessionmaker, Session

from .database import engine

logger = logging.getLogger("medicine.backend.db.session")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a SQLAlchemy session per request,
    guaranteeing rollback on error and cleanup on completion.
    """
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.error(f"Database transaction error: {e}")
        raise
    finally:
        db.close()
