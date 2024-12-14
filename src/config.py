from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGO: str
    ACCESS_TOKEN_EXP: int
    REFRESH_TOKEN_EXP: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
