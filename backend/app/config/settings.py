from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://ecotrack_user:ecotrack_pass@localhost:35432/ecotrack"
    REDIS_URL: str = "redis://localhost:36379/0"
    SECRET_KEY: str = "ecotrack-super-secret-key-change-in-production-abc123def456"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
