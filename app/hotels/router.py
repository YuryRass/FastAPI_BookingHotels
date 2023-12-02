from datetime import date
from fastapi import APIRouter

from app.hotels.dao import HotelDAO
from app.hotels.models import Hotels
from app.hotels.shemas import SFreeHotels, SHotel

router: APIRouter = APIRouter(
    prefix='/hotels',
    tags=["All hotels"]
)


@router.get("/{location}")
async def get_all_hotels(
    location: str, date_from: date, date_to: date
) -> list[SFreeHotels]:

    """Вывод всех свободных отелей на текущие даты

    Args:

        location (str): расположение отеля

        date_from (date): дата заезда

        date_to (date): дата выезда

    Returns:

        list[SFreeHotels]: список свободных отелей
    """
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotel:
    """Вывод отеля по его ID

    Args:
        hotel_id (int): ID отеля

    Returns:

        SHotel: информация об отели
    """
    hotel: Hotels | None = await HotelDAO.get_hotel(hotel_id)
    return hotel
