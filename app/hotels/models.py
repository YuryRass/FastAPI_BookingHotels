"""
    Класс, реализующий модель 'Отели'
    и его дочерниюю модель 'Комнаты'
"""
from sqlalchemy import JSON, ForeignKey
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


class Rooms(Base):
    """Комнаты отелей"""
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    # hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
