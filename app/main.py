from fastapi import FastAPI

from app.api.routers import api_router
from app.core.managers import redis


def startup_tasks():
    app.router.include_router(
        api_router
    )


async def close_redis():
    print('close_redis')
    await redis.close()

app = FastAPI(
    on_startup=[startup_tasks],
    on_shutdown=[close_redis]
)
