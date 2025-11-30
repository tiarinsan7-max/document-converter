"""
Application Configuration Settings
"""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application Info
    APP_NAME: str = "Universal Document Converter"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Convert documents between multiple formats"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    OUTPUT_DIR: Path = BASE_DIR / "outputs"
    LOG_DIR: Path = BASE_DIR / "logs"
    RULES_DIR: Path = BASE_DIR / "Rules"
    WORKFLOWS_DIR: Path = BASE_DIR / "Workflows"
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: List[str] = [
        '.pdf', '.docx', '.xlsx', '.csv', '.json', '.txt'
    ]
    
    # Conversion Settings
    DEFAULT_QUALITY: str = "high"
    ENABLE_OCR: bool = True
    PRESERVE_FORMATTING: bool = True
    
    # Supported Formats
    SUPPORTED_FORMATS: List[str] = [
        'pdf', 'docx', 'xlsx', 'csv', 'json', 'txt'
    ]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    
    # Security
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8501",
    ]
    
    # Performance
    MAX_WORKERS: int = 4
    CHUNK_SIZE: int = 8192
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure directories exist
settings.UPLOAD_DIR.mkdir(exist_ok=True)
settings.OUTPUT_DIR.mkdir(exist_ok=True)
settings.LOG_DIR.mkdir(exist_ok=True)
