"""Конечные точки для бронирования отелей"""

from datetime import date

from fastapi import APIRouter, Depends, Response, status

from app.bookings.dependecies import get_bookings_service
from app.bookings.service import BookingsService
from app.bookings.shemas import BookingsAll, SBookings
from app.users.auth.jwt_auth.dependencies import get_current_user
from app.users.models import Users

router: APIRouter = APIRouter(prefix="/bookings", tags=["Бронирование отелей"])


@router.get(
    "",
    summary="Список всех броней",
    response_model=list[BookingsAll],
    response_model_exclude_none=True,
)
async def get_bookings(
    user: Users = Depends(get_current_user),
    booking_service: BookingsService = Depends(get_bookings_service),
):
    """
    Возвращает информацию по бронированиям отелей
    для авторизованного пользователя.
    """
    return await booking_service.get_all_bookings(user.id)


@router.get(
    "/{booking_id}",
    summary="Получение конкретной брони",
    response_model=SBookings | None,
    response_model_exclude_none=True,
)
async def get_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
    booking_service: BookingsService = Depends(get_bookings_service),
):
    """
    Возвращает информацию по брони для авторизованного пользователя.
    """
    return await booking_service.get_booking(booking_id, user.id)


@router.post(
    "",
    summary="Бронирование отеля",
    response_model=SBookings,
    response_model_exclude_none=True,
)
async def add_booking_for_user(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
    booking_service: BookingsService = Depends(get_bookings_service),
):
    """
    Добавляет информацию по бронированию отеля
    для авторизованного пользователя.
    """

    return await booking_service.add_booking_for_user(
        user.id,
        room_id,
        date_from,
        date_to,
    )


@router.delete("/{booking_id}", summary="Удаление брони")
async def delete_booking(
    booking_id: int,
    response: Response,
    user: Users = Depends(get_current_user),
    booking_service: BookingsService = Depends(get_bookings_service),
):
    """
    Удаление информации о бронировани (по ID брони)
    для текущего пользователя.
    """
    booking = await booking_service.delete_booking(user.id, booking_id)
    if booking:
        response.status_code = status.HTTP_204_NO_CONTENT
