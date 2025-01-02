from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Endpoint Security AI Agent"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    RELOAD: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = "duckdb:///./data/edr.db"
    TEST_DATABASE_URL: str = "duckdb:///./data/test.db"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    MODELS_DIR: Path = BASE_DIR / "models"
    DATA_DIR: Path = BASE_DIR / "data"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # AI/ML
    ML_MODEL_PATH: str = os.getenv("ML_MODEL_PATH", str(MODELS_DIR / "ransomware_detector"))
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # osquery
    OSQUERY_SOCKET: str = os.getenv("OSQUERY_SOCKET", "/var/osquery/osquery.sock")
    OSQUERY_CONFIG: str = os.getenv("OSQUERY_CONFIG", str(BASE_DIR / "config" / "osquery.conf"))
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create directories if they don't exist
os.makedirs(Settings().MODELS_DIR, exist_ok=True)
os.makedirs(Settings().DATA_DIR, exist_ok=True)
os.makedirs(Settings().LOGS_DIR, exist_ok=True)

settings = Settings()
