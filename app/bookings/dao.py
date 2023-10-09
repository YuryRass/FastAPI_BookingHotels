"""Класс, реализующий CRUD-операции к модели 'Бронирования'"""
from bookings.models import Bookings
from dao.base import BaseDAO


class BookingsDAO(BaseDAO):
    """DAO объект 'Бронирования'"""
    model = Bookings
