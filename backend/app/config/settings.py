from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_NAME: str = "RIVA"
    VERSION: str = "1.0.0"

    API_PREFIX: str = "/api"


settings = Settings()