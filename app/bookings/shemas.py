"""Pydantic-схема 'Бронирования отелей'"""
from datetime import date

from pydantic import BaseModel


class SBookings(BaseModel):
    """Бронирования отелей"""

    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int | None = None
    total_days: int | None = None
    image_id: int | None = None
    name: str | None = None
    description: str | None = None
    services: list[str] | None = None

    class Config:
        """атрибут from_attributes позволяет обращаться
        к pydantic-модели, как к ORM модели
        """

        from_attributes = True
