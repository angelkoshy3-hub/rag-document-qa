import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings and environment variables.
    Using pydantic-settings for robust configuration management.
    """
    # App Information
    APP_NAME: str = "FastAPI RAG System"
    API_V1_STR: str = "/api/v1"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Storage Configuration
    UPLOAD_DIR: str = "data/raw_docs"
    VECTOR_DB_DIR: str = "data/vector_db"

    # Pydantic configuration to read from env files
    model_config = SettingsConfigDict(case_sensitive=True)

# Instantiate settings singleton to be used across the app
settings = Settings()
