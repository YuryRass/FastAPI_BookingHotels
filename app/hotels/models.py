"""
    Класс, реализующий модель 'Отели'
"""
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotels(Base):
    """Отели"""
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]

    # rooms: Mapped[list["Rooms"]] = relationship(
    #     back_populates="hotel",
    #     cascade="all, delete-orphan"
    # )
