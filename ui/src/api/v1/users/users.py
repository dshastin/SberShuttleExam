from typing import Annotated
from fastapi import APIRouter, Depends, Request, Body, Form
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_db
from models import UserSchemaCreate, User
from services.users import UserService, get_user_service

router = APIRouter()


@router.get("/", response_model=list[UserSchemaCreate], tags=['Users'])
async def get_all_users(request: Request, db: AsyncSession = Depends(get_db)):
    users = await User.get_all(db)
    return users


@router.get("/{login}", response_model=UserSchemaCreate, tags=['Users'])
async def get_user_by_login(request: Request, login: str, db: AsyncSession = Depends(get_db)):
    user = await User.get_by_login(db, login=login)
    return user


@router.post("/{login}/update", response_model=UserSchemaCreate, tags=['Users'])
async def update_user(request: Request, login: str,
                      email: Annotated[str, Form()],
                      password: Annotated[str, Form()],
                      first_name: Annotated[str, Form()],
                      middle_name: Annotated[str, Form()],
                      last_name: Annotated[str, Form()],
                      user_service: UserService = Depends(get_user_service)):
    new_user_data = dict(
        login=login,
        email=email,
        password=password,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name
    )
    user = await user_service.update_user_info(login, new_user_data)
    return user
