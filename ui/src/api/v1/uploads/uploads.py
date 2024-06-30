import shutil

from fastapi import APIRouter, UploadFile
from models.db.images import Image
from db.postgres import get_db

router = APIRouter()
db = get_db()


@router.post("/upload_files/", tags=["Uploads"], summary="Upload a file", )
async def create_upload_file(files: list[UploadFile]):
    uploaded_files = []
    for file in files:
        # save file info to db
        await Image.create(db, filename=file.filename, size=file.size)

        file_path = f'static/{file.filename}'
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    return {"filenames": [f.filename for f in files]}
