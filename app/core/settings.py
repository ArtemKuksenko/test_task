from pydantic import BaseSettings

from app.utils.utils import load_env


class Settings(BaseSettings):
    API_APP_PORT: int

    # redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str


load_env()
settings = Settings()
