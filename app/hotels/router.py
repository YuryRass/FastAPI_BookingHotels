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
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotel:
    hotel: Hotels | None = await HotelDAO.get_hotel(hotel_id)
    return hotel
