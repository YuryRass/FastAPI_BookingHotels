from datetime import date

from fastapi import APIRouter

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.shemas import SRooms

router: APIRouter = APIRouter(prefix="/hotels", tags=["Комнаты отелей"])


@router.get("/{hotel_id}/rooms", summary="Список все комнат")
async def get_all_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRooms]:
    """Получает список всех комнат для конкретного отеля
    Args:

        hotel_id (int): ID отеля
        date_from (date): дата заезда
        date_to (date): дата выезда

    Returns:

        list[SRooms]: список всех номеров
    """
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)
    return rooms
