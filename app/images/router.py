import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import modify_picture

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


@router.post("/holels")
async def add_hotel_image(name_id: int, file: UploadFile):
    """Добавление картинки отеля в локальную папку

    Args:

        name_id (int): ID картинки в БД

        file (UploadFile): загруженный через инструменты FastAPI файл
    """
    img_path: str = f"app/static/images/{name_id}.webp"
    with open(img_path, "wb+") as file_obj:
        shutil.copyfileobj(file.file, file_obj)
    modify_picture(img_path)
