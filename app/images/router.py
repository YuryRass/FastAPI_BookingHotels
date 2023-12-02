import shutil
from fastapi import APIRouter, UploadFile

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


@router.post("/holels")
async def add_hotel_image(name_id: int, file: UploadFile):
    with open(f"app/static/images/{name_id}.webp", "wb+") as file_obj:
        shutil.copyfileobj(file.file, file_obj)
