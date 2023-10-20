from fastapi import FastAPI

from app.bookings.router import router as bookings_router
from app.users.router import router as user_router
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as rooms_router

app: FastAPI = FastAPI()
app.include_router(user_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)


@app.get(path="/hotels")
def get_hotels():
    return "Отель гранд 5 звёзд"
