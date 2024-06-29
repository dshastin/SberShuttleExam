from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, Column, select
from sqlalchemy.ext.asyncio import AsyncSession


class UUIDModelMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)


class CreatedAtMixin:
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now)


class BaseCRUDModelMixin:
    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        model = cls(**kwargs)
        db.add(model)
        await db.commit()
        await db.refresh(model)
        return model

    @classmethod
    async def get(cls, db: AsyncSession, id: UUID):
        return await db.get(cls, id)

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()
