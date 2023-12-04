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
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: str
    services: list[str]

    class Config:
        """атрибут from_attributes позволяет обращаться
        к pydantic-модели, как к ORM модели
        """
        from_attributes = True
