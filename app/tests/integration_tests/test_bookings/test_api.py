import pytest
from httpx import AsyncClient, Response


@pytest.mark.parametrize(
    "room_id,date_from,date_to,booked_rooms,status_code",
    *[
        [(4, "2030-05-01", "2030-05-15", i, 200) for i in range(3, 11)]
        + [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
    ],
)
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    booked_rooms,
    authenticated_ac: AsyncClient,
):
    response: Response = await authenticated_ac.post(
        url="/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code

    response: Response = await authenticated_ac.get(url="/bookings")

    assert booked_rooms == len(response.json())
