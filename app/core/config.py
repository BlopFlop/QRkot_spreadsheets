import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from pydantic import BaseSettings, EmailStr

from app.core.constants import DATE_FORMAT, LOG_DIR, LOG_FORMAT


class Settings(BaseSettings):
    """Settings for current project."""

    # Fast Api Project
    app_title: str = "Благотворительный фонд поддержки котиков QRKot"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "secret"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    # Google services
    type: Optional[str]
    project_id: Optional[str]
    private_key_id: Optional[str]
    private_key: Optional[str]
    client_email: Optional[str]
    client_id: Optional[str]
    auth_uri: Optional[str]
    token_uri: Optional[str]
    auth_provider_x509_cert_url: Optional[str]
    client_x509_cert_url: Optional[str]
    email: Optional[str]

    class Config:
        env_prefix = "QRK_"
        env_file = ".env"


def configure_logging() -> None:
    """Configure logging from this project."""
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / "qr_kot_logging.log"
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10**6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DATE_FORMAT,
        format=LOG_FORMAT,
        level=logging.WARNING,
        handlers=(rotating_handler, logging.StreamHandler()),
    )


settings = Settings()
