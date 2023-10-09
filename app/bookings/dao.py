"""Класс, реализующий CRUD-операции к модели 'Бронирования'"""
from app.bookings.models import Bookings
from app.dao.base import BaseDAO


class BookingsDAO(BaseDAO):
    """DAO объект 'Бронирования'"""
    model = Bookings
