from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    BACKEND_URL: str  # ← AÑADIDO

    class Config:
        env_file = ".env"

settings = Settings()
