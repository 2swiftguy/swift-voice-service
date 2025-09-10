from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TWILIO_SID: str
    TWILIO_TOKEN: str

    PYTHON_VOICE_TOKEN: str
    PYTHON_SMS_TOKEN: str

    OPENAI_API_KEY: str | None = None
    REDIS_URL: str = "redis://localhost:6379/0"
    ENV: str = "local"
    PUBLIC_BASE_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env.local", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
