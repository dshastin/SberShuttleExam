from fastapi import APIRouter, Body, Depends, Request
from services.users import UserService, get_user_service

from models import UserSchemaCreate, UserSchemaCreateSuccess

register_router = APIRouter(prefix="/register")


@register_router.post(
    "/",
    response_model=UserSchemaCreateSuccess,
    summary="Register new user",
    description="Creates a new user with the provided information.",
    tags=["Authentication"],
)
async def register_user(
        request: Request,
        user: UserSchemaCreate = Body(),
        user_service: UserService = Depends(get_user_service),
) -> UserSchemaCreateSuccess:
    """
    Creates a new user with the provided information.

    :param user: UserSchemaCreate The user information for registration.
    :param user_service: UserService An instance of UserService for user registration.
    :return: UserSchemaCreateSuccess model containing the created user information.
    """
    user = await user_service.create_user(user)
    return user
