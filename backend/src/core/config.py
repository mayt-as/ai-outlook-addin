from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Outlook AI Add-in API"
    debug: bool = False
    
    # Auth
    client_id: str = "your-client-id"
    client_secret: str = "your-client-secret"
    tenant_id: str = "common"
    
    # AI Provider
    openai_api_key: str = "your-openai-key"
    openai_api_base: str = "https://api.openai.com/v1"
    fallback_api_key: str = "your-fallback-key"
    fallback_api_base: str = "https://api.fallback.com/v1"
    primary_model: str = "gpt-4"
    fallback_model: str = "gpt-3.5-turbo"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
