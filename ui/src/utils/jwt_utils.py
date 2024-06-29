import hashlib

from fastapi import Request
from jose import JWTError, jwt

from core import settings
from core.logger import logger
from models import User
from services.postgres import sessionmanager


async def parse_token_with_getting_user(full_token: str) -> User | None:
    token: str = full_token.split(" ").pop()
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("email")
        if email is None:
            return None
    except JWTError:
        return None
    async with sessionmanager.session() as session:
        user = await User.get_by_email(session, email)
    if user is None:
        return None
    return user


async def validate_token(request: Request):
    full_token: str | None = request.headers.get("Authorization")
    if full_token is None:
        return None
    user: User | None = await parse_token_with_getting_user(full_token)
    if user is None:
        return None

    request.state.user = user
    logger.info(f"success validating token for user {user.login}")
    return request
