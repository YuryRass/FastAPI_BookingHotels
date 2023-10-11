"""Класс, реализующий CRUD-операции к модели 'Бронирования'"""
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.dao.base import BaseDAO
from database import async_session_maker
from datetime import date
from sqlalchemy import select, insert, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession


class BookingsDAO(BaseDAO):
    """DAO объект 'Бронирования'"""
    model = Bookings

    @classmethod
    async def add_booking(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ) -> Bookings | None:
        """Осуществляет бронирование комнаты, если есть свободные номера

        Args:
            user_id (int): ID пользователя
            room_id (int): ID комнаты
            date_from (date): дата заселения
            date_to (date): дата выезда

        Returns: Bookings | None
        """
        # получаем забронированные комнаты на заданную дату
        booked_rooms = (
            select(Bookings).
            where(
                and_(
                    Bookings.room_id == room_id,
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
            )
        ).cte("booked_rooms")

        session: AsyncSession
        async with async_session_maker() as session:
            get_rooms_left = (
                select(Rooms.quantity - func.count(booked_rooms.c.room_id)).
                select_from(Rooms).
                join(booked_rooms, Rooms.id == booked_rooms.c.room_id).
                where(Rooms.id == room_id).
                group_by(Rooms.quantity, booked_rooms.c.room_id)
            )
            # Получаем свободные комнаты на заданные даты
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                # получаем цену за комнату, которую хотят забронить
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()

                stmt = (
                    insert(Bookings).
                    values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    ).
                    returning(Bookings)
                )
                new_booking: Bookings = await session.execute(stmt)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
