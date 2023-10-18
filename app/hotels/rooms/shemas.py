"""Pydantic-схема 'Комнаты отелей'"""
from pydantic import BaseModel


class SRooms(BaseModel):
    """Схема для вывода информации о комнатах"""
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int

    class Config:
        """атрибут from_attributes позволяет обращаться
        к pydantic-модели, как к ORM модели
        """
        from_attributes = True
