from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DB_NAME: str
    DB_USER: str
    DB_PORT: int
    DB_PW: str
    TEST_DB: str

    PJ_TITLE: str


settings = Setting()
