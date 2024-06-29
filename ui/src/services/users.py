import hashlib
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from uuid import UUID

from fastapi import Depends, HTTPException, status
from jose import jwt
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import and_
from werkzeug.security import generate_password_hash

from core.config import settings
from db.postgres import get_db
from models import (
    JWToken,
    User,
    UserSchemaChangeLogin,
    UserSchemaChangePassword,
    UserSchemaCreate,
    UserSchemaCreateSuccess,
)
from models.schemas import RefreshedToken


class UserService:
    """Service for users."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def login_user(self, user: User, user_agent: str):
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        user_data: UserSchemaCreateSuccess = UserSchemaCreateSuccess.model_validate(user)
        user_data.role_name = user.role.role if user.role is not None else None
        payload_data = user_data.model_dump(mode="json")
        access_token = self.create_jwt_token(
            data=payload_data, expires_delta=access_token_expires, token_type="access"
        )
        refresh_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        refresh_token = self.create_jwt_token(
            data=payload_data,
            expires_delta=refresh_token_expires,
            token_type="refresh",
        )
        await self.put_refresh_token_to_db(refresh_token, refresh_token_expires, user, user_agent)
        return JWToken(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def create_jwt_token(
            data: dict, expires_delta: timedelta | None = None, token_type: str = "access"
    ):
        """
        Creates a JSON Web Token for user authentication.

        :param data: dict The data to be encoded in the JWT.
        :param expires_delta: timedelta | None The expiration time delta for the token.
        :param token_type: str The type of token to be created (e.g., "access" or "refresh").
        :return: str The encoded JWT token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            if token_type == "access":
                expire = datetime.now(timezone.utc) + timedelta(minutes=15)
            else:
                expire = datetime.now(timezone.utc) + timedelta(minutes=3000)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )
        return encoded_jwt

    async def change_login(self, user_id: UUID, user_data: UserSchemaChangeLogin):
        """
        Changes the login for a user.

        :param user_id: str The unique identifier of the user.
        :param user_data: UserSchemaChangeLogin The new login information for the user.
        :raises: HTTPException If the user is not found.
        """
        user: User = await User.get(self.db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        check_login_exist_user = await User.get_by_login(self.db, user_data.login)
        if check_login_exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="login already exists"
            )
        user.login = user_data.login
        await self.db.commit()

    async def change_password(self, user_id: UUID, user_data: UserSchemaChangePassword):
        """
        Changes the password for a user.

        :param user_id: str The unique identifier of the user.
        :param user_data: UserSchemaChangePassword The new password information for the user.
        :raises: HTTPException If the user is not found.
        """
        user: User = await User.get(self.db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        user.password = generate_password_hash(user_data.old_password)
        await self.db.commit()

    async def create_user(self, user_data: UserSchemaCreate) -> User:
        """
        Creates a new user with the provided information.

        :param user_data: UserSchemaCreate The data for creating the new user.
        :return: UserModel The newly created user object.
        """
        await User.create(self.db, **user_data.model_dump())
        user: User = await User.get_by_email(self.db, email=user_data.email)
        return user

    async def get_user_by_id(self, user_id: UUID):
        """
        Retrieves a user by unique identifier.

        :param user_id: UUID The unique identifier of the user.
        :return: UserModel The retrieved user object.
        """
        user: User = await User.get(self.db, user_id)
        return user

    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a user by email address.

        :param email: str The email address of the user.
        :return: UserModel The retrieved user object.
        """
        user: User = await User.get_by_email(self.db, email)
        return user

    async def get_user_by_login(self, login: str) -> User:
        """
        Retrieves a user by login.

        :param login: str The email address of the user.
        :return: UserModel The retrieved user object.
        """
        user: User = await User.get_by_login(self.db, login)
        return user

    async def put_refresh_token_to_db(
            self,
            refresh_token: str,
            refresh_token_expires: timedelta,
            user: User,
            user_agent: str,
    ):
        """
        Stores the refresh token and its expiration in the database for the specified user.

        :param refresh_token: str The refresh token to be stored.
        :param refresh_token_expires: timedelta The expiration duration for the refresh token.
        :param user: UserSchemaBase The user for whom the refresh token is stored.
        :param user_agent: str The user agent associated with the token.
        :return: None

        """
        expire: datetime = datetime.now(timezone.utc) + refresh_token_expires
        device: Device = await Device.create_or_update(
            self.db,
            name=user_agent,
            user=user,
            refresh_token=refresh_token,
            expires_in=int(expire.timestamp()),
        )
        await AccessHistory.create(self.db, device=device)

    async def refresh_access_token(self, user: User, token: str) -> RefreshedToken:
        """
        Generates a new access token using the refresh token.

        :param user: User | None current user
        :param token: str An instance of refresh token.
        :return: RefreshedToken containing the new access token.
        """
        refresh_token: str = token.split(" ").pop()
        refresh_hash = hashlib.md5(f"refresh_token:{refresh_token}".encode("utf-8")).hexdigest()
        if cached_token is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token in blacklist"
            )
        device_query: Select = select(Device).where(
            and_(Device.user_id == user.id, Device.refresh_token == refresh_token)
        )
        result = await self.db.execute(device_query)
        device = result.scalars().first()
        if device is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token"
            )
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self.create_jwt_token(
            data={"email": user.email}, expires_delta=access_token_expires
        )
        return RefreshedToken(access_token=access_token)


@lru_cache()
def get_user_service(
        db: AsyncSession = Depends(get_db)
) -> UserService:
    return UserService(db)
