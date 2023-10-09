"""Конечные точки для бронирования отелей"""
from fastapi import APIRouter
from app.bookings.dao import BookingsDAO
from app.bookings.shemas import SBookings

router: APIRouter = APIRouter(
    prefix="/bookings",
    tags=["Бронирование отелей"]
)


@router.get("")
async def get_bookings() -> list[SBookings]:
    """Возвращает информацию по всем бронированиям

    Returns:
        list[SBookings]: список всех броней
    """
    return await BookingsDAO.find_all()
