import asyncio

from fastapi.routing import APIRouter

from app.core.managers import run_generator

router = APIRouter(prefix="/calculate", tags=["calculatesomething"])


@router.get("/")
@run_generator
async def calculate():
    print("run")
    for i in range(15):
        await asyncio.sleep(1)
        yield

    yield {"result": "ok"}
