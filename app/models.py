from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str = ""
    guest_auth_token: str = "secret_guest_token"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')

settings = Settings()
