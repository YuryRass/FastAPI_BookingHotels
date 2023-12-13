from fastapi import APIRouter, File, Response, UploadFile, status

from app.importer.init_model import init_model

router: APIRouter = APIRouter(
    prefix="/import",
    tags=["Заполнение моделей из csv файлов"],
)


@router.post("/{model}")
async def init_hotels_model(
    model: str, response: Response, uploaded_file: UploadFile = File(...)
):
    await init_model(model, uploaded_file.file)
    response.status_code = status.HTTP_201_CREATED
