from fastapi.routing import APIRouter
from app.api.v1 import (
    calculate
)

api_router = APIRouter(
    prefix='/api'
)
api_router.include_router(calculate.router)
