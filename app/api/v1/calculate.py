from fastapi.routing import APIRouter

router = APIRouter(prefix="/calculate", tags=["calculatesomething"])


@router.post("/")
async def ping():
    return "pong"
