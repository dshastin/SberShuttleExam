from api.v1.auth import auth_router
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
