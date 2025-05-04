"""Модель пользователей"""
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.bookings.models import Bookings


class Users(Base):
    """Пользователи сайта Booking"""

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        return f"User: {self.email}"
