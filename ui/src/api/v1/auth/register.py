from typing import Annotated
from fastapi import APIRouter, Body, Depends, Request, Form

from models import UserSchemaCreate, UserSchemaCreateSuccess
from services.users import UserService, get_user_service

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
    user = await user_service.create_user(user)
    return user


@register_router.post(
    "/form",
    response_model=UserSchemaCreateSuccess,
    summary="Register new user",
    description="Creates a new user with the provided information.",
    tags=["Authentication"],
)
async def register_user_form(
        request: Request,
        login: Annotated[str, Form()],
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        first_name: Annotated[str, Form()],
        middle_name: Annotated[str, Form()],
        last_name: Annotated[str, Form()],
        user_service: UserService = Depends(get_user_service),
) -> UserSchemaCreateSuccess:
    user_form = UserSchemaCreate(login=login,
                                 email=email,
                                 password=password,
                                 first_name=first_name,
                                 middle_name=middle_name,
                                 last_name=last_name)
    user = await user_service.create_user(user_form)
    return user
