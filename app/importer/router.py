from fastapi import APIRouter, File, HTTPException, Response, UploadFile, status
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.importer.init_model import SQLModel, init_model

router: APIRouter = APIRouter(
    prefix="/import",
    tags=["Заполнение моделей из csv файлов"],
)


@router.post("/{model}")
async def init_model_from_csv_file(
    model: SQLModel,
    response: Response,
    uploaded_file: UploadFile = File(...),
):
    """Инициализация SQL модели посредством считывания данных из csv файла

    Args:
        model (str): SQL модель

        response (Response): HTTP ответ

        uploaded_file (UploadFile, optional): CSV файл. Defaults to File(...).
    """

    try:
        await init_model(model, uploaded_file.file)
    except ValidationError:
        raise HTTPException(
            status_code=400,
            detail=f"Validation error in the file {uploaded_file.filename}",
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=400,
            detail="SQLAlchemy exception: Item insert error",
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Incorrect data in the file {uploaded_file.filename}",
        )

    response.status_code = status.HTTP_201_CREATED
