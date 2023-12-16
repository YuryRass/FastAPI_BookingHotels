from datetime import date

import pytest

from app.hotels.dao import HotelDAO


@pytest.mark.parametrize(
    "location,date_from,date_to,rooms_left",
    [
        ("Алтай", date(2023, 6, 5), date(2023, 6, 30), 13),
        ("Алтай", date(2023, 4, 5), date(2023, 4, 30), 14),
    ],
)
async def test_find_all_hotels(
    location: str,
    date_from: date,
    date_to: date,
    rooms_left: int,
):
    all_hotels = await HotelDAO.find_all(
        location=location,
        date_from=date_from,
        date_to=date_to,
    )

    assert location in all_hotels[0]["location"]
    assert all_hotels[0]["rooms_left"] == rooms_left

