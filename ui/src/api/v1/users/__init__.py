from fastapi import APIRouter

from .users import router

users_router = APIRouter(prefix='/users')
users_router.include_router(router)
