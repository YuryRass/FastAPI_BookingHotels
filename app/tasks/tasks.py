from pathlib import Path

from httpx import AsyncClient
from PIL import Image

from app.config import settings
from app.tasks.celery import celery


@celery.task
def modify_picture(path: str):
    """Создает два изображения с размерами 400х200 и 1000х500

    Args:
        path (str): путь до изображения, которое будет изменяться
    """
    img_path = Path(path)
    img = Image.open(img_path)

    for width, height in [(400, 200), (1000, 500)]:
        resized_img = img.resize(size=(width, height))
        resized_img.save(f"app/static/images/resized_{width}_{height}_{img_path.name}")


@celery.task
async def send_message_to_telegram_user(msg: str):
    """Отправка сообщения телеграм пользователю

    Args:
        msg (str): сообщение для отправки
    """
    async with AsyncClient(base_url=settings.TG_SEND_MESSAGE_URL) as client:
        await client.post(
            url="/sendMessage",
            data={
                "chat_id": settings.TG_USER_ID,
                "text": msg,
            },
        )
