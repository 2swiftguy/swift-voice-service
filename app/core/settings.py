from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SERVICE_AUTH_TOKEN: str
    OPENAI_API_KEY: str | None = None
    REDIS_URL: str = "redis://localhost:6379/0"
    ENV: str = "local"
    PUBLIC_BASE_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env.local.local", env_file_encoding="utf-8")

settings = Settings()