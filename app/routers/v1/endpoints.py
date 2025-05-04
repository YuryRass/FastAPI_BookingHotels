from fastapi import APIRouter

from app.bookings.router import router as bookings_router
from app.hotels.rooms.router import router as rooms_router
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.importer.router import router as importer_router
from app.pages.router import router as pages_router
from app.prometheus.router import router as prometheus_router
from app.users.router import router as user_router

api_router = APIRouter()

routers = (
    bookings_router,
    rooms_router,
    hotels_router,
    images_router,
    importer_router,
    pages_router,
    prometheus_router,
    user_router,
)

for router in routers:
    api_router.include_router(router)
