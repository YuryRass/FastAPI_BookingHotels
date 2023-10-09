"""Класс, реализующий CRUD-операции к модели 'Пользователи'"""
from dao.base import BaseDAO
from users.models import Users


class UsersDAO(BaseDAO):
    """DAO объект 'Пользователи'"""
    model = Users
