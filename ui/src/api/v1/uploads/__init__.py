from fastapi import APIRouter
from .uploads import router as upload_file_router


uploads_router = APIRouter(prefix='/uploads')
uploads_router.include_router(upload_file_router)
