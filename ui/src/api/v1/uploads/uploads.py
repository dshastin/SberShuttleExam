import shutil

from fastapi import APIRouter, UploadFile, Depends, Request

from core.logger import logger
from db.postgres import get_db
from models import Image, ImageModel

router = APIRouter()


@router.get("/get_all", tags=["Uploads"], response_model=list[ImageModel])
async def get_uploaded_files(request: Request, db=Depends(get_db)):
    all_images: list[Image] = await Image.get_all(db)
    logger.info(f"Got {len(all_images)}")
    return all_images


@router.post("/upload_files/", tags=["Uploads"], summary="Upload a file", )
async def create_upload_file(files: list[UploadFile], db=Depends(get_db)):
    uploaded_files = []
    for file in files:
        # save file info to db
        img_info = {'filename': file.filename, 'size': file.size}
        uploaded_files.append(img_info)
        await Image.create(db, **img_info)

        file_path = f'static/{file.filename}'
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    logger.info(f'uploaded {len(uploaded_files)} files')
    return uploaded_files
