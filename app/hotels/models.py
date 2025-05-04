"""
    Класс, реализующий модель 'Отели'
"""
from typing import TYPE_CHECKING

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.hotels.rooms.models import Rooms


class Hotels(Base):
    """Отели"""

    name: Mapped[str] = mapped_column(unique=True)
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]

    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")

    def __str__(self) -> str:
        return f"Hotel: '{self.name}'"
