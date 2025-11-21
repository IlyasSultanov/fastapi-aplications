from pathlib import Path
from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=str(ENV_FILE), case_sensitive=False, extra='ignore')

    app_port: int = Field(description="Port project", alias="APP_PORT")
    app_reload: bool = Field(description="Reload app", default=True)

    project_name: str = Field(description="", alias="PROJECT_NAME")
    version: str = Field(description="", alias="VERSION")
    description: str = Field(description="", alias="DESCRIPTION", default="")
    debug: bool = Field(description="", alias="DEBUG")
    cors_allow_credentials: bool = Field(description="", alias="CORS_ALLOW_CREDENTIALS", default=True)

    db_url: str = Field(alias="DATABASE_URL")


settings = Settings()  # type: ignore
