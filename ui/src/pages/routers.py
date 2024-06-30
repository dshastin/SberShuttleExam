from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from api.v1.uploads.uploads import get_uploaded_files

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
async def get_files(request: Request, images=Depends(get_uploaded_files)):
    return templates.TemplateResponse("gallery.html", {"request": request, 'images': images})