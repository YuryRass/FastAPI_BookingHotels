"""Реализация модели 'Бронирования'"""

from datetime import date
from sqlalchemy import ForeignKey, Date, Computed
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Bookings(Base):
    """Таблица 'Бронирования'"""

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(
        Computed("(date_to - date_from) * price")
    )
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))
