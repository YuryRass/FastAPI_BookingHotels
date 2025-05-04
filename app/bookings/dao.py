"""Класс, реализующий CRUD-операции к модели 'Бронирования'"""

from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.exceptions import NoFreeRoomsException
from app.hotels.rooms.models import Rooms
from app.infrastructure.database import async_session_maker
from app.logger import logger
from app.users.models import Users


class BookingsDAO(BaseDAO):
    """DAO объект 'Бронирования'"""

    model = Bookings

    @classmethod
    async def add_booking(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """Осуществляет бронирование комнаты, если есть свободные номера

        Args:
            user_id (int): ID пользователя
            room_id (int): ID комнаты
            date_from (date): дата заселения
            date_to (date): дата выезда

        Returns:
        """

        try:
            # Получаем кол-во свободных комнат на заданные даты
            rooms_left = await cls._get_left_rooms(
                room_id=room_id,
                date_from=date_from,
                date_to=date_to,
            )

            if rooms_left > 0:
                session: AsyncSession
                async with async_session_maker() as session:
                    # получаем цену за комнату, которую хотят забронить
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    _price = await session.execute(get_price)
                    price = _price.scalar()
                res = await super().add(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                )
                return res
            else:
                raise NoFreeRoomsException

        except NoFreeRoomsException:
            raise NoFreeRoomsException
        except (SQLAlchemyError, Exception) as exc:
            msg = None
            if isinstance(exc, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(exc, Exception):
                msg = "Unknown Exc: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)

    @classmethod
    async def all_bookings(cls, user_id: int):
        """Выводит все бронирования пользователя

        Args:
            user_id (int): ID пользователя
        """
        all_bookings_query = (
            select(cls.model)
            .options(joinedload(cls.model.room))
            .options(joinedload(cls.model.user).load_only(Users.email))
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
    async def _get_left_rooms(
        cls,
        room_id: int,
        date_from: date,
        date_to: date,
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
            _rooms_left = await session.execute(get_rooms_left)
            return _rooms_left.scalar_one()


async def get_bookings_dao() -> BookingsDAO:
    return BookingsDAO()
