from fastapi import FastAPI

from app.api.routers import api_router
from app.core.managers import redis, run_generator, logger


def startup_tasks():
    app.router.include_router(
        api_router
    )


async def close_redis():
    await redis.close()


async def clear_run_generator_data():
    try:
        await run_generator.clear_redis_data()
    except Exception as ex:
        logger.error(ex)

app = FastAPI(
    on_startup=[startup_tasks],
    on_shutdown=[clear_run_generator_data, close_redis]
)
