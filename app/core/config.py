from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DB_NAME: str
    DB_USER: str = "postgres"
    DB_PORT: int = 5432
    DB_PW: str
    TEST_DB: str = "test_db"

    CORS_ORIGINS: str = ["*"]

    PJ_TITLE: str


settings = Setting()
