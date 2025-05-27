import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / 'venv'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Shanyraq.kz"
    VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./shanyraq.db")

settings = Settings()

