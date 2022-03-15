from run_single_generator import RunSingleGenerator

from .logger import Logger
from .settings import settings
from app.utils import utils

redis = utils.create_redis_client(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD
)

logger = Logger("run_single_generator").logger
run_generator = RunSingleGenerator(redis, "my_app", logger)
