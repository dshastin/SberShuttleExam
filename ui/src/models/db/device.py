from sqlalchemy import UUID, BigInteger, Column, ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from services.postgres import Base
from .mixins import BaseCRUDModelMixin, CreatedAtMixin, UUIDModelMixin
from .user import User as UserModel


class Device(Base, UUIDModelMixin, CreatedAtMixin, BaseCRUDModelMixin):
    __tablename__ = "devices"

    name = Column(String(255), nullable=False)
    fingerprint = Column(String(64), unique=True, index=True, nullable=True)
    refresh_token = Column(String(2048), unique=True, index=True, nullable=False)
    expires_in = Column(BigInteger, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="devices")

    @classmethod
    async def create_or_update(
            cls, db: AsyncSession, name: str, user: UserModel, refresh_token: str, expires_in: int
    ) -> "Device":
        result = await db.execute(select(cls).filter_by(name=name, user_id=user.id))
        device = result.scalars().first()

        if device is not None:
            device.refresh_token = refresh_token
        else:
            device = cls(name=name, user=user, refresh_token=refresh_token, expires_in=expires_in)
        db.add(device)
        await db.commit()
        await db.refresh(device)
        return device

    def __repr__(self) -> str:
        return f"<Device {self.name}>"
