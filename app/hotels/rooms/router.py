from datetime import date
from fastapi import APIRouter

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.shemas import SRooms


router: APIRouter = APIRouter(
    prefix="/hotels",
    tags=["Get all rooms"]
)


@router.get("/{hotel_id}/rooms")
async def get_all_rooms(
    hotel_id: int, date_from: date, date_to: date
) -> list[SRooms]:
    """Получает список всех комнат для конкретного отеля"""
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)
    return rooms
