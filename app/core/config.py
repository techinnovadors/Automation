import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # Base settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Project"

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Environment settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Google settings
    GOOGLE_API_KEY: str
    GOOGLE_GENAI_USE_VERTEXAI: bool = False
    GOOGLE_CLOUD_PROJECT: str | None = None
    GOOGLE_CLOUD_LOCATION: str | None = None

    # Tavily settings
    TAVILY_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
