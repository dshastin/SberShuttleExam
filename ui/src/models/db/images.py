from sqlalchemy import BigInteger, Column, String
from sqlalchemy import Column, DateTime, Boolean
from services.postgres import Base
from .mixins import BaseCRUDModelMixin, CreatedAtMixin, UUIDModelMixin
from datetime import datetime


class Image(Base, UUIDModelMixin, CreatedAtMixin, BaseCRUDModelMixin):
    __tablename__ = "images"

    filename = Column(String(255), nullable=False)
    size = Column(BigInteger, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now())
