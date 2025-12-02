import os
from pydantic_settings import BaseSettings

# Allow all origins in production
if os.getenv('RENDER'):
    cors_origins: list = ['*']
else:
    cors_origins: list = ['http://localhost:8000', 'http://127.0.0.1:8000']

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    app_name: str = "Freelancer Portfolio API"
    app_version: str = "1.0.0"
    app_description: str = "Manage freelancer profiles and ratings"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = int(os.environ.get("PORT", 8000))
    debug: bool = os.environ.get("DEBUG", "False").lower() == "true"
    
    # Database Settings
    db_path: str = os.environ.get("DB_PATH", "/app/data/freelancer.db")
    
    # CORS Settings
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()

# Ensure database directory exists
os.makedirs(os.path.dirname(settings.db_path), exist_ok=True)