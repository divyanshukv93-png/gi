from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str  # required: no default, never hardcode
    access_token_minutes: int = 60
    cors_origins: str = "http://localhost:5173"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    data_gov_api_key: str = ""
    market_resource_id: str = ""
    iot_device_token: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
