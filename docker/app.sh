#!/bin/bash

alembic upgrade head

gunicorn app.main:app -c app/gunicorn.conf.py