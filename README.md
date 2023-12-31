# Бронирование отелей

Веб-приложение, написанное на языке Python с примененем асинхронного фреймворка FastAPI. В приложении задействованы следующие технологии: SQLAlchemy, Celery, Redis, Docker.

Схема базы данных веб-приложения выглядит следующим образом:
![](/readme_images/db.jpg)

## Запуск приложения

Для запуска FastAPI используется веб-сервер uvicorn. Команда для запуска выглядит так:

```
uvicorn app.main:app --reload
```

Ее необходимо запускать в командной строке, обязательно находясь в корневой директории проекта.

### Celery & Flower

Для запуска Celery используется команда

```
celery --app=app.tasks.celery:celery worker -l INFO
```

Для запуска Flower используется команда

```
celery --app=app.tasks.celery:celery flower
```

### Dockerfile

Для запуска веб-сервера (FastAPI) внутри контейнера необходимо раскомментировать код внутри Dockerfile и иметь уже запущенный экземпляр PostgreSQL на компьютере.
Код для запуска Dockerfile:

```
docker build .
```

Команда также запускается из корневой директории, в которой лежит файл Dockerfile.

### Docker compose

Для запуска всех сервисов (БД, Redis, веб-сервер (FastAPI), Celery, Flower, Grafana, Prometheus) необходимо использовать файл docker-compose.yml и команды

```
docker compose build
docker compose up
```

Причем `build` команду нужно запускать, только если вы меняли что-то внутри Dockerfile, то есть меняли логику составления образа.
