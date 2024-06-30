from fastapi import APIRouter

# from api.v1.auth.change import change_router
from api.v1.auth.login import login_router
from api.v1.auth.refresh_token import refresh_token_router
from api.v1.auth.register import register_router

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(register_router)
auth_router.include_router(login_router)
# auth_router.include_router(change_router)
auth_router.include_router(refresh_token_router)
