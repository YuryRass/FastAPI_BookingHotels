"""Pydantic-схема 'Свободные отели'"""
from decimal import Decimal

from pydantic import BaseModel


class SFreeHotels(BaseModel):
    """Схема для вывода информации о свободных отелях"""

    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    rooms_left: Decimal

    class Config:
        """атрибут from_attributes позволяет обращаться
        к pydantic-модели, как к ORM модели
        """

        from_attributes = True


class SHotel(BaseModel):
    id: int | None = None
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
