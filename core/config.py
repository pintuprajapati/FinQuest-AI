import os
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_ACCESS_TOKEN: str
    ENVIRONMENT: str
        
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", False)
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI App")

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # New GenAI settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./vector_db")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Redis Settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # OpenAI Settings
    OPENAI_API_KEY: str
    
    # Document storage
    STATIC_DIR: str = os.getenv("STATIC_DIR", "./static")
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", "16777216"))  # 16MB

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

@lru_cache()
def get_settings():
    return Settings()

# Load settings
settings = get_settings() 
