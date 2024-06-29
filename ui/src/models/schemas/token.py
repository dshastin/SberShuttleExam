from pydantic import BaseModel, Field


class RefreshedToken(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
