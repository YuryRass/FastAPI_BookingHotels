"""Конечные точки для бронирования отелей"""
from datetime import date
from fastapi import APIRouter, Depends
from app.bookings.dao import BookingsDAO
from app.bookings.shemas import SBookings
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.bookings.models import Bookings
from exceptions import NoFreeRoomsException

router: APIRouter = APIRouter(
    prefix="/bookings",
    tags=["Бронирование отелей"]
)


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user)
) -> list[SBookings]:
    """Возвращает информацию по бронированиям отелей
    для пользователя, который зашел на сайт

    Returns:
        list[SBookings]: список всех броней
    """
    return await BookingsDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
):
    booking: Bookings = await BookingsDAO.add_booking(
        user.id, room_id, date_from, date_to
    )
    if not booking:
        raise NoFreeRoomsException
    return booking
