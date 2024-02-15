import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    MODE1: Literal["DEV", "TEST", "PROD"]  
    LOG_LEVEL: str

    POSTGRES_DB: str 
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str 

    @property
    def DATABASE_URL(self): 
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    TEST_POSTGRES_DB1: str
    TEST_POSTGRES_USER1: str
    TEST_POSTGRES_PASSWORD1: str
    TEST_POSTGRES_HOST1: str
    TEST_POSTGRES_PORT1: str

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_POSTGRES_USER1}:{self.TEST_POSTGRES_PASSWORD1}@{self.TEST_POSTGRES_HOST1}:{self.TEST_POSTGRES_PORT1}/{self.TEST_POSTGRES_DB1}"

    SECRET_KEY8: str
    PUBLIC_KEY8: str
    ALGORITHM: str

    ADMIN_SECRET_KEY: str
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: float = 0.007

    CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]
    CORS_METHODS: list[str]

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()