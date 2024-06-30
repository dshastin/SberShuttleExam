from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory='templates')


@router.get('/login/')
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get('/users/')
def users(request: Request):
    return 'coming soon'


@router.get('/uploads')
def get_base_template(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.get("/gallery")
async def get_files(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request, 'images': ['1', '2', '3']})