FROM python:3.11

RUN mkdir /booking

WORKDIR /booking

RUN pip install poetry

COPY poetry.lock pyproject.toml /booking/

RUN poetry install

COPY . /booking

RUN chmod a+x /booking/docker/*.sh

# RUN alembic upgrade head

CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]