import asyncio

from fastapi.routing import APIRouter

from app.core.managers import run_generator

router = APIRouter(prefix="/calculate", tags=["calculatesomething"])


@router.post("/")
@run_generator
async def calculate():
    """
    Генератор эмулирующий выполнение алгоритма
    :return:
    """
    for i in range(15):
        await asyncio.sleep(1)
        yield

    yield {"result": "ok"}
