from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, String, Text, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from models.db.mixins import BaseCRUDModelMixin, CreatedAtMixin, UUIDModelMixin
from services.postgres import Base


class User(Base, UUIDModelMixin, CreatedAtMixin, BaseCRUDModelMixin):
    __tablename__ = "users"

    login = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    middle_name = Column(String(50), nullable=True)

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = generate_password_hash(kwargs["password"])
        return await super().create(db, **kwargs)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str) -> Optional["User"]:
        result = await db.execute(select(cls).where(cls.email == email))
        return result.scalars().first()

    @classmethod
    async def get_by_login(cls, db: AsyncSession, login: str) -> Optional["User"]:
        result = await db.execute(select(cls).where(cls.login == login))
        return result.scalars().first()

    def __repr__(self) -> str:
        return f"<User {self.login}>"

