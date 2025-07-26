from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    decade: str
    century: str
    target_words_path: str
    cors_origins: list[str] = []

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()