from pathlib import Path

from PIL import Image

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
        resized_img.save(
            f"app/static/images/resized_{width}_{height}_{img_path.name}"
        )
