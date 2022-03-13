from run_single_generator import RunSingleGenerator

from app.core.settings import settings
from app.utils import utils

redis = utils.create_redis_client(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD
)

run_generator = RunSingleGenerator(redis, "my_app")
