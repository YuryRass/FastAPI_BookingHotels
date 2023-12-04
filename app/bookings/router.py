"""Конечные точки для бронирования отелей"""

from datetime import date

from fastapi import APIRouter, Depends, Response, status

from app.bookings.dao import BookingsDAO
from app.bookings.models import Bookings
from app.exceptions import NoFreeRoomsException
from app.users.dependencies import get_current_user
from app.users.models import Users

# from app.bookings.shemas import SBookings

router: APIRouter = APIRouter(
    prefix="/bookings",
    tags=["Бронирование отелей"]
)


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user)
):  # -> list[SBookings]:
    """Возвращает информацию по бронированиям отелей
    для авторизованного пользователя

    Args:

        user (Users, optional): текущий пользователь

    Defaults to Depends(get_current_user)
    """

    return await BookingsDAO.all_bookings(user_id=user.id)


@router.post("")
async def add_booking_for_user(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
):
    """Добавляет информацию по бронированию отеля
    для авторизованного пользователя

    Args:

        room_id (int): ID комнаты

        date_from (date): дата заезда

        date_to (date): дата выезда

        user (Users, optional): текущий авторизованный пользователь.

    Raises:

        NoFreeRoomsException: нет свободных комнат
    """

    booking: Bookings = await BookingsDAO.add_booking(
        user.id, room_id, date_from, date_to
    )
    if not booking:
        raise NoFreeRoomsException
    return booking


@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    response: Response,
    user: Users = Depends(get_current_user)
):
    """Удаление информации о бронировани (по ID брони)
    для текущего пользователя

    Args:

        booking_id (int): ID бронирования

        response (Response): HTTP ответ

        user (Users, optional): текущий пользователь.

    Defaults to Depends(get_current_user).
    """
    booking = await BookingsDAO.delete_booking(user.id, booking_id)
    if booking:
        response.status_code = status.HTTP_204_NO_CONTENT
