from fastapi import FastAPI

from app.api.routers import api_router


def startup_tasks():
    app.router.include_router(
        api_router
    )


app = FastAPI(
    on_startup=[startup_tasks],
)
