import pydantic_settings
from pydantic import Field
from functools import lru_cache

class Settings(pydantic_settings.BaseSettings):

    database_url: str = Field(default="sqlite:///./allocations.db")

    model_config = pydantic_settings.SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore",
            case_sensitive=False
            )
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
