import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEFAULT_ENV_FILE = BASE_DIR / ".env"
ENV_FILE_OVERRIDE = os.getenv("SETTINGS_ENV_FILE")

if ENV_FILE_OVERRIDE:
    override_path = Path(ENV_FILE_OVERRIDE)
    ENV_FILE = override_path if override_path.exists() else None
elif DEFAULT_ENV_FILE.exists():
    ENV_FILE = DEFAULT_ENV_FILE
else:
    ENV_FILE = None


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE else None,
        case_sensitive=False,
        extra="ignore",
    )
    # =====================================================================================================
    # Configurations for jwt
    # =====================================================================================================
    private_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expires_minutes: int = 30
    refresh_token_expires_minutes: int = 60 * 24 * 14  # 14 days by default
    issuer: str = "ai-assistant-chat"
    audience: str = "ai-assistant-clients"

    # =====================================================================================================
    # Configurations with about prject
    # =====================================================================================================
    app_port: int = Field(description="Port project", alias="APP_PORT")
    app_reload: bool = Field(description="Reload app", default=True)

    project_name: str = Field(description="", alias="PROJECT_NAME")
    version: str = Field(description="", alias="VERSION")
    description: str = Field(description="", alias="DESCRIPTION", default="")
    debug: bool = Field(description="", alias="DEBUG")
    cors_allow_credentials: bool = Field(description="", alias="CORS_ALLOW_CREDENTIALS", default=True)

    db_url: str = Field(alias="DATABASE_URL")

    # =====================================================================================================
    # Configurations with celery
    # =====================================================================================================
    # celery_broker_url: str = Field(description="Url for broker for celery", alias="CELERY_BROKER_URL")
    # celery_result_backend: str = Field(description="Url for backend", alias="CELERY_RESULT_BACKEND")

settings = Settings()  # type: ignore
