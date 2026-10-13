"""
Central Application Configuration Module.
Loads environment variables from .env files and provides typed settings.
"""

import os
from pathlib import Path
from typing import List, Optional

# Determine Project Roots
CURRENT_FILE = Path(__file__).resolve()
BACKEND_ROOT = CURRENT_FILE.parent.parent.parent  # backend/
PROJECT_ROOT = BACKEND_ROOT.parent               # workspace root /

# Automatically load .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    # Check backend/.env first, then root .env
    if (BACKEND_ROOT / ".env").exists():
        load_dotenv(BACKEND_ROOT / ".env")
    elif (PROJECT_ROOT / ".env").exists():
        load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass


class Settings:
    """Application Settings and Configuration."""

    # General App Settings
    PROJECT_NAME: str = "Medicine AI Backend API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Directory Paths
    PROJECT_ROOT_PATH: Path = PROJECT_ROOT
    BACKEND_ROOT_PATH: Path = BACKEND_ROOT
    ML_TRAINING_DIR: Path = PROJECT_ROOT / "ml_training"
    DATASETS_DIR: Path = PROJECT_ROOT / "datasets"

    # Security & Upload Validation
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "15"))
    MAX_UPLOAD_SIZE_BYTES: int = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    MAX_IMAGE_PIXELS: int = 50_000_000

    # CORS Configuration
    CORS_ORIGINS_RAW: str = os.getenv("CORS_ORIGINS", "*")

    @property
    def cors_origins(self) -> List[str]:
        if self.CORS_ORIGINS_RAW.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS_RAW.split(",") if origin.strip()]

    # Database Configuration (Placeholders)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "medicine_db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    _DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", None)

    @property
    def database_url(self) -> str:
        """
        Constructs database connection string or returns direct DATABASE_URL override.
        """
        if self._DATABASE_URL and self._DATABASE_URL.strip():
            return self._DATABASE_URL.strip()
        
        # If DB_PASSWORD or DB_USER provided, construct PostgreSQL connection URL
        if self.DB_USER and self.DB_PASSWORD:
            return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
        # Local development fallback
        return f"sqlite:///{self.BACKEND_ROOT_PATH / 'medicine.db'}"

    # OCR Settings
    OCR_LANGUAGES: List[str] = [lang.strip() for lang in os.getenv("OCR_LANGUAGES", "en").split(",") if lang.strip()]
    OCR_USE_GPU: bool = os.getenv("OCR_USE_GPU", "false").lower() in ("true", "1", "yes")


settings = Settings()
