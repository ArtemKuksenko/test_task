from pydantic import BaseSettings

from app.utils.utils import load_env


class Settings(BaseSettings):
    API_APP_PORT: int


load_env()
settings = Settings()
