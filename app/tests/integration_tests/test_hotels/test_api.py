from datetime import date

import pytest
from httpx import AsyncClient, Response


@pytest.mark.parametrize(
    "date_from,date_to,status_code",
    [
        (date(2030, 12, 12), date(2030, 12, 24), 200),
        (date(2030, 12, 24), date(2030, 12, 12), 400),
        (date(2030, 10, 24), date(2030, 12, 24), 400),  # diff > 30 days
    ],
)
async def test_get_all_hotels(
    ac: AsyncClient, date_from: str, date_to: str, status_code: int
):
    resp: Response = await ac.get(
        url="/hotels/Алтай",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert resp.status_code == status_code


@pytest.mark.parametrize(
    "hotel_id,status_code",
    [
        (1, 200),
        (2, 200),
        (100, 400),
    ],
)
async def test_get_hotel(ac: AsyncClient, hotel_id: int, status_code: int):
    resp: Response = await ac.get(
        url=f"/hotels/id/{hotel_id}",
    )

    assert resp.status_code == status_code
