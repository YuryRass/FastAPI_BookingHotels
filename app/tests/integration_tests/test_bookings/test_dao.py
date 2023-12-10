from datetime import date

import pytest

from app.bookings.dao import BookingsDAO
from app.bookings.models import Bookings


@pytest.mark.parametrize(
    "user_id,room_id",
    [
        (2, 2),
        (2, 3),
        (1, 4),
        (1, 4),
    ],
)
async def test_booking_crud(user_id: int, room_id: int):
    # Add booking
    added_booking: Bookings = await BookingsDAO.add_booking(
        user_id=user_id,
        room_id=room_id,
        date_from=date(2023, 12, 12),
        date_to=date(2023, 12, 24),
    )

    assert added_booking.user_id == user_id
    assert added_booking.room_id == room_id

    # Find booking
    booking_id = added_booking.id
    finded_booking: Bookings = await BookingsDAO.find_one_or_none(id=booking_id)

    assert added_booking == finded_booking

    # Delete booking
    await BookingsDAO.delete_booking(user_id, booking_id)

    finded_booking: Bookings | None = await BookingsDAO.find_one_or_none(id=booking_id)

    assert finded_booking is None
