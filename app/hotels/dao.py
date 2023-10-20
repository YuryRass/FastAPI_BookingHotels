"""Класс, реализующий CRUD-операции к модели 'Hotels'"""
from datetime import date
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from sqlalchemy import func, select, and_, or_

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.database import engine, async_session_maker


class HotelDAO(BaseDAO):
    """CRUD-операции для Hotels"""
    model = Hotels

    @classmethod
    async def find_all(
        cls,
        location: str,
        date_from: date,
        date_to: date
    ):
        """Получение списка отелей

        Args:
            location (str): расположение отеля
            date_from (date): дата заезда в отель
            date_to (date): дата выезда из отеля
        """
        # получаем список забронированных комнат на заданную дату
        booked_rooms = (
            select(Bookings).
            where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from
                    )
                )
            )
        ).cte("booked_rooms")

        conn: AsyncConnection
        async with engine.connect() as conn:
            # новое кол-во свободных комнат (с учетом бронирования)
            # для таблицы Rooms
            new_rooms_quantity = (
                select(
                    Rooms,
                    (
                        Rooms.quantity -
                        func.count(
                            booked_rooms.c.room_id
                        ).filter(
                            booked_rooms.c.room_id.is_not(None)
                        )
                    ).label('new_quantity')
                )
                .select_from(Rooms)
                .join(
                    booked_rooms, Rooms.id == booked_rooms.c.room_id,
                    isouter=True
                )
                .group_by(Rooms.id, Rooms.quantity, booked_rooms.c.room_id)
            ).cte('new_rooms_quantity')

            # незанятые отели (где кол-во комнат > 0)
            free_hotels_query = (
                select(
                    Hotels,
                    func.sum(
                        new_rooms_quantity.c.new_quantity
                    ).label('rooms_left')
                )
                .select_from(Hotels)
                .join(
                    new_rooms_quantity,
                    new_rooms_quantity.c.hotel_id == Hotels.id
                )
                .where(Hotels.location.contains(location))
                .group_by(Hotels.id)
                .having(
                    func.sum(
                        new_rooms_quantity.c.new_quantity
                    ).label('rooms_left') > 0
                )
            )

            free_hotels = await conn.execute(free_hotels_query)
            return free_hotels.all()

    @classmethod
    async def get_hotel(
        cls,
        hotel_id: int
    ):
        get_hotel_query = (
            select(Hotels)
            .where(Hotels.id == hotel_id)
        )

        session: AsyncSession
        async with async_session_maker() as session:
            res = await session.execute(get_hotel_query)
            return res.scalar()
