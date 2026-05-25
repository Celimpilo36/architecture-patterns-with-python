from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):

    database_url: str = Field(default="sqlite:///./allocations.db")

    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore",
            case_sensitive=False
            )
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
