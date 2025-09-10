from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    DB_URL: str
    DATABASE_URL_TEST: str = "sqlite:///:memory:"
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool = False
    BASE_URL: str = "http://localhost:3000"
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "test@example.com"
    SMTP_PASSWORD: SecretStr = SecretStr("fake-password")
    SMTP_FROM: str = "test@example.com"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
