from dataclasses import dataclass
from datetime import date
from typing import Any

from app.bookings.cache import BookingCache
from app.bookings.dao import BookingsDAO
from app.bookings.models import Bookings
from app.bookings.shemas import SBookings
from app.exceptions import NoFreeRoomsException


@dataclass
class BookingsService:
    bookings_dao: BookingsDAO
    booking_cache: BookingCache

    async def get_all_bookings(self, user_id: int) -> list[Bookings]:
        return await BookingsDAO.all_bookings(user_id)

    async def get_booking(
        self,
        booking_id: int,
        user_id: int,
    ) -> SBookings | None:
        booking = await self.booking_cache.get_booking(booking_id)

        if not booking:
            if booking := await self.bookings_dao.find_one_or_none(
                id=booking_id, user_id=user_id
            ):
                await self.booking_cache.set_booking(booking)

        return booking

    async def add_booking_for_user(
        self,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> Any | None:
        booking = await BookingsDAO.add_booking(
            user_id,
            room_id,
            date_from,
            date_to,
        )
        if not booking:
            raise NoFreeRoomsException
        await self.booking_cache.set_booking(booking)
        return booking

    async def delete_booking(self, user_id: int, booking_id: int) -> int | None:
        if await BookingsDAO.delete_booking(user_id, booking_id):
            await self.booking_cache.delete_booking(booking_id)
            return booking_id
