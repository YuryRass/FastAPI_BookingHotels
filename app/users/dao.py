"""Класс, реализующий CRUD-операции к модели 'Пользователи'"""
from app.dao.base import BaseDAO
from app.users.models import Users


class UsersDAO(BaseDAO):
    """DAO объект 'Пользователи'"""

    model = Users
