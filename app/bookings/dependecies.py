from fastapi import Depends
from redis.asyncio import Redis

from app.bookings.cache import BookingCache
from app.bookings.dao import BookingsDAO, get_bookings_dao
from app.bookings.service import BookingsService
from app.infrastructure.cache import get_cache


async def get_bookings_cache(
    redis_cache: Redis = Depends(get_cache),
) -> BookingCache:
    return BookingCache(redis_cache)


async def get_bookings_service(
    bookings_dao: BookingsDAO = Depends(get_bookings_dao),
    bookings_cache: BookingCache = Depends(get_bookings_cache),
) -> BookingsService:
    return BookingsService(bookings_dao, bookings_cache)
