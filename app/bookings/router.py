"""Конечные точки для бронирования отелей"""
from fastapi import APIRouter, Depends
from app.bookings.dao import BookingsDAO
from app.bookings.shemas import SBookings
from app.users.dependencies import get_current_user
from app.users.models import Users

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
