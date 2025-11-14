from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    SUPABASE_URL: str = Field(...)
    SUPABASE_SERVICE_ROLE_KEY: str = Field(...)

    MEILISEARCH_URL: str = Field(...)
    MEILISEARCH_MASTER_KEY: str = Field(...)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()