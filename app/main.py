from fastapi import FastAPI

from app.api.routers import api_router
from app.core.managers import redis, run_generator


def startup_tasks():
    app.router.include_router(
        api_router
    )


async def close_redis():
    await redis.close()


async def clear_run_generator_data():
    await run_generator.clear_redis_data()


app = FastAPI(
    on_startup=[startup_tasks],
    on_shutdown=[clear_run_generator_data, close_redis]
)
