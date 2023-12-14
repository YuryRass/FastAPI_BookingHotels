"""Модуль, реализующий CRUD-опреации для модели 'Rooms'"""
from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    """CRUD-операции для Rooms"""

    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        """Возвращает список всех номеров комнат
        определенного отеля для конкретных дат

        Args:
            hotel_id (int): ID отеля
            date_from (date): дата заезда
            date_to (date): дата выезда
        """

        # получаем забронированные комнаты на заданную дату
        # для всех отелей
        booked_rooms = (
            select(Bookings).where(
                and_(
                    Bookings.date_from < date_to,
                    Bookings.date_to > date_from,
                )
            )
        ).cte("booked_rooms")

        get_rooms_query = (
            select(
                Rooms.__table__.columns,
                (Rooms.price * (date_to - date_from).days).label("total_cost"),
                (
                    Rooms.quantity
                    - func.count(booked_rooms.c.room_id).filter(
                        booked_rooms.c.room_id.isnot(None)
                    )
                ).label("rooms_left"),
            )
            .select_from(Rooms)
            .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
            .where(Rooms.hotel_id == hotel_id)
            .group_by(Rooms.id, Rooms.quantity, booked_rooms.c.room_id)
        ).cte("get_rooms_query")

        res = await super().get_all(get_rooms_query)
        return res
