from functools import lru_cache
from typing import List
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings
from typing_extensions import Annotated


class Settings(BaseSettings):
    """Application settings with validation and caching."""
    # Database
    DATABASE_URL: PostgresDsn = "postgresql://postgres:postgres@db:5432/fastapi_db"
    ASYNC_DATABASE_URL: PostgresDsn = "postgresql+asyncpg://postgres:postgres@db:5432/fastapi_db"
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    APP_NAME: str = "FastAPI App Template"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = []
    CORS_HEADERS: List[str] = ["*"]
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "env_file_encoding": "utf-8"
    }

    @field_validator("CORS_ORIGINS", mode="before")
    def validate_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Validate CORS_ORIGINS from env."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str):
            return eval(v)
        return v


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Create settings instance
settings = get_settings()
