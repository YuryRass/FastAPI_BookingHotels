from fastapi import FastAPI
import uvicorn
from app.bookings.router import router as bookings_router
from app.users.router import router as user_router


app: FastAPI = FastAPI()
app.include_router(user_router)
app.include_router(bookings_router)


@app.get(path="/hotels")
def get_hotels():
    return "Отель гранд 5 звёзд"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8089, reload=True)
