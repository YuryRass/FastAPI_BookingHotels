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


async def test_get_and_delete_bookings(authenticated_ac: AsyncClient):
    response: Response = await authenticated_ac.get(url="/bookings")
    user_bookings = response.json()

    assert len(user_bookings) > 0

    # Циклически удаляем все брони авторизованного пользователя
    for booking in user_bookings:
        response: Response = await authenticated_ac.delete(
            url=f"/bookings/{booking['id']}",
        )
        assert response.status_code == 204

    # Снова получаем пользовательские брони, которых уже нет
    response: Response = await authenticated_ac.get(url="/bookings")
    user_bookings = response.json()

    assert not user_bookings
