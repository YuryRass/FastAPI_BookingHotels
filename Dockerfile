FROM python:3.11

RUN mkdir /booking

WORKDIR /booking

RUN pip install poetry

COPY poetry.lock pyproject.toml /booking/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . /booking

RUN chmod a+x /booking/docker/*.sh
