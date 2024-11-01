from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str 
    GEMINI_API_KEY: str
    GEMINI_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 