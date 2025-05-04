import json

from redis.asyncio import Redis

from app.bookings.models import Bookings
from app.bookings.shemas import SBookings


class BookingCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_booking(self, booking_id: int) -> SBookings | None:
        if booking := await self.redis.get(f"booking_{booking_id}"):
            return SBookings.model_validate(json.loads(booking))

    async def set_booking(self, booking: Bookings) -> None:
        booking_schema = SBookings.model_validate(booking)
        await self.redis.set(
            f"booking_{booking.id}",
            booking_schema.model_dump_json(exclude_none=True),
        )

    async def delete_booking(self, booking_id: int) -> None:
        await self.redis.delete(f"booking_{booking_id}")
