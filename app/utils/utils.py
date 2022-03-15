import os
import aioredis
from dotenv import load_dotenv


def load_env():
    dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../.env.config')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


def create_redis_client(
        host: str,
        port: int,
        db: int,
        password: str
) -> aioredis.StrictRedis:
    return aioredis.StrictRedis(connection_pool=aioredis.ConnectionPool(
        host=host,
        port=port,
        db=db,
        password=password
    ))
