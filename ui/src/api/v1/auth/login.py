from fastapi import APIRouter, Body, Depends, Header, HTTPException, Request, status, Form
from typing import Annotated
from models import JWToken, UserSchemaBase
from services.users import UserService, get_user_service

login_router = APIRouter(prefix="/login")


@login_router.post(
    "/",
    summary="Create access and refresh tokens for user",
    tags=["Authentication"],
    status_code=status.HTTP_201_CREATED,
)
async def login(
        request: Request,
        user_agent: str = Header(default=None),
        user: UserSchemaBase = Body(),
        user_service: UserService = Depends(get_user_service),
) -> JWToken:
    """
    Generates access and refresh tokens for user authentication and authorization.

    :param user_agent: str The user agent string for the request.
    :param user: UserSchemaBase The user information for authentication.
    :param user_service: UserService An instance of UserService for user authentication.
    :return: JWTToken containing access and refresh tokens for the user.
    """
    user = await user_service.authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens: JWToken = await user_service.login_user(user=user, user_agent=user_agent)
    return tokens


@login_router.post('/login_form', tags=["Authentication"])
async def login_form(
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        user_agent: str = Header(default=None),
        user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens: JWToken = await user_service.login_user(user=user, user_agent=user_agent)
    return tokens
