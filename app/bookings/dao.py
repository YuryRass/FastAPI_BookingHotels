"""Класс, реализующий CRUD-операции к модели 'Бронирования'"""
from datetime import date
from sqlalchemy import select, delete, insert, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.dao.base import BaseDAO
from app.users.models import Users
from app.database import async_session_maker, engine


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

        # Получаем кол-во свободных комнат на заданные даты
        rooms_left: int = await cls._get_left_rooms(
            room_id, date_from, date_to
        )

        if rooms_left > 0:
            session: AsyncSession
            async with async_session_maker() as session:
                # получаем цену за комнату, которую хотят забронить
                get_price = select(Rooms.price).filter_by(id=room_id)
                _price = await session.execute(get_price)
                price: int = _price.scalar()

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
                new_booking = await session.execute(stmt)
                await session.commit()
                return new_booking.scalar()
        else:
            return None

    @classmethod
    async def all_bookings(
        cls,
        user_id: int
    ):
        all_bookings_query = (
            select(
                Bookings.room_id,
                Bookings.user_id,
                Bookings.date_from,
                Bookings.date_to,
                Rooms.price,
                Bookings.total_cost,
                Bookings.total_days,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services
            )
            .select_from(Users)
            .join(Bookings, Users.id == Bookings.user_id)
            .join(Rooms, Bookings.room_id == Rooms.id)
            .where(Users.id == user_id)
        )
        conn: AsyncConnection
        async with engine.connect() as conn:
            user_bookings = await conn.execute(all_bookings_query)
            return user_bookings.all()

    @classmethod
    async def delete_booking(
        cls,
        user_id: int,
        booking_id: int
    ):
        delete_booking_query = (
            delete(Bookings)
            .where(
                and_(
                    Bookings.id == booking_id,
                    Bookings.user_id == user_id
                )

            )
            .returning(Bookings)
        )

        session: AsyncSession
        async with async_session_maker() as session:
            res = await session.execute(delete_booking_query)
            await session.commit()
            return res.scalar()

    async def _get_left_rooms(
        cls,
        room_id: int,
        date_from: date,
        date_to: date
    ) -> int:
        """Возвращает кол-во свободных комнат на заданные даты

        Args:
            room_id (int): ID комнаты
            date_from (date): дата засесения
            date_to (date): дата выезда

        Returns:
            int: количество свободных комнат
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

            return rooms_left
