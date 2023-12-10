"""Класс, реализующий CRUD-операции к модели 'Бронирования'"""

from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class BookingsDAO(BaseDAO):
    """DAO объект 'Бронирования'"""

    model = Bookings

    @classmethod
    async def add_booking(
        cls, user_id: int, room_id: int, date_from: date, date_to: date
    ):
        """Осуществляет бронирование комнаты, если есть свободные номера

        Args:
            user_id (int): ID пользователя
            room_id (int): ID комнаты
            date_from (date): дата заселения
            date_to (date): дата выезда

        Returns:
        """

        # Получаем кол-во свободных комнат на заданные даты
        rooms_left: int = await cls._get_left_rooms(
            room_id=room_id, date_from=date_from, date_to=date_to
        )

        if rooms_left > 0:
            session: AsyncSession
            async with async_session_maker() as session:
                # получаем цену за комнату, которую хотят забронить
                get_price = select(Rooms.price).filter_by(id=room_id)
                _price = await session.execute(get_price)
                price: int = _price.scalar()

            res = await super().add(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price,
            )
            return res
        else:
            return None

    @classmethod
    async def all_bookings(cls, user_id: int):
        """Выводит все бронирования пользователя

        Args:
            user_id (int): ID пользователя
        """
        all_bookings_query = (
            select(
                cls.model
            )
            .options(selectinload(cls.model.room))
            .options(selectinload(cls.model.user).load_only(Users.email))
            .where(cls.model.user_id == user_id)
        )
        session: AsyncSession
        async with async_session_maker() as session:
            res = await session.execute(all_bookings_query)
            return res.scalars().all()

    @classmethod
    async def delete_booking(cls, user_id: int, booking_id: int):
        """Удаляет информацию о бронировании по его ID

        Args:
            user_id (int): ID пользователя
            booking_id (int): ID брони
        """
        res = await super().delete_records(id=booking_id, user_id=user_id)

        return res

    @classmethod
    async def _get_left_rooms(cls, room_id: int, date_from: date, date_to: date) -> int:
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
            select(cls.model).where(
                and_(
                    cls.model.room_id == room_id,
                    Bookings.date_from < date_to,
                    Bookings.date_to > date_from,
                )
            )
        ).cte("booked_rooms")

        session: AsyncSession
        async with async_session_maker() as session:
            get_rooms_left = (
                select(
                    Rooms.quantity
                    - func.count(booked_rooms.c.room_id).filter(
                        booked_rooms.c.room_id.is_not(None)
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )
            # Получаем свободные комнаты на заданные даты
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            return rooms_left
