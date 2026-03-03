import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    STORAGE_DIR: str = "storage"
    
    class Config:
        env_file = ".env"

settings = Settings()

if not os.path.exists(settings.STORAGE_DIR):
    os.makedirs(settings.STORAGE_DIR)
