from datetime import datetime

from pydantic import BaseModel


class ImageModel(BaseModel):
    filename: str
    size: int
    uploaded_at: datetime
