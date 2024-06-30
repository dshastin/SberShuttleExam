from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from models import User
from models.schemas import RefreshedToken
from services.users import UserService, get_user_service
from utils.jwt_utils import parse_token_with_getting_user

refresh_token_router = APIRouter()


@refresh_token_router.post(
    "/refresh/",
    response_model=RefreshedToken,
    summary="Refresh access token",
    description="Generates a new access token using the refresh token.",
    tags=["Authentication"],
    status_code=status.HTTP_201_CREATED,
)
async def refresh(
        authorization: Annotated[str | None, Header()] = None,
        user_service: UserService = Depends(get_user_service),
) -> RefreshedToken:
    """
    Generates a new access token using the refresh token.

    :param authorization: str | None The authorization token for refreshing the access token.
    :param user_service: UserService An instance of UserService for user token management.
    :return: RefreshedToken containing the new access token.
    """
    print(authorization)
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided",
        )
    user: User | None = await parse_token_with_getting_user(authorization)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    new_token: RefreshedToken = await user_service.refresh_access_token(user, authorization)
    return new_token
