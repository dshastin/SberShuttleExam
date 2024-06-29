from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSchemaBase(BaseModel):
    email: str
    password: str


class UserSchemaCreate(UserSchemaBase):
    login: str
    first_name: str
    middle_name: str | None = None
    last_name: str


class UserSchemaFull(UserSchemaBase):
    id: UUID
    company_name: str
    company_post: str


class UserSchemaBase(BaseModel):
    email: EmailStr
    password: str


class UserSchema(UserSchemaBase):
    id: str
    model_config = ConfigDict(from_attributes=True)


class UserSchemaCreateSuccess(BaseModel):
    id: UUID
    login: str
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserSchemaChangeLogin(BaseModel):
    login: str
    model_config = ConfigDict(from_attributes=True)


class UserSchemaChangePassword(BaseModel):
    old_password: str
    new_password: str
    model_config = ConfigDict(from_attributes=True)


class JWToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default="bearer")


class JWTokenData(BaseModel):
    email: str
