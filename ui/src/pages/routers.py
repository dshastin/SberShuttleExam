from fastapi import APIRouter, Request, Depends

from api.v1.uploads.uploads import get_uploaded_files
from api.v1.users.users import get_all_users, get_user_by_login
from core.config import templates

router = APIRouter(tags=['Pages'])


@router.get('/')
def login(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get('/register/')
def login(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get('/login/')
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get('/users/')
def users(request: Request, users_list=Depends(get_all_users)):
    return templates.TemplateResponse("users.html", {"request": request, "users_list": users_list})


@router.get('/users/{login}')
def users(request: Request, user=Depends(get_user_by_login)):
    return templates.TemplateResponse("user_update.html", {"request": request, "user": user})


@router.get('/uploads')
def get_base_template(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.get("/gallery")
async def get_files(request: Request, images=Depends(get_uploaded_files)):
    return templates.TemplateResponse("gallery.html", {"request": request, 'images': images})
