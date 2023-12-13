import csv
from pathlib import Path
from typing import BinaryIO

from app.bookings.dao import BookingsDAO
from app.bookings.shemas import SBookings
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.shemas import SRooms
from app.hotels.shemas import SHotel

shemes: dict[str, SHotel] = {
    "hotels": SHotel,
    "bookings": SBookings,
    "rooms": SRooms,
}

dao: dict[str, HotelDAO] = {
    "hotels": HotelDAO,
    "bookings": BookingsDAO,
    "rooms": RoomDAO,
}


async def init_model(model: str, f_io: BinaryIO):
    # save csv to local dir
    csv_path = Path.cwd().joinpath("app").joinpath("csv")
    csv_path.mkdir(exist_ok=True)
    file_path = csv_path.joinpath(f"{model}.csv")

    with open(file_path, mode="wb+") as f:
        f.write(f_io.read())

    smodel = shemes[model]
    # read csv and convert to json
    csv_data: list[dict] = []
    with open(file_path, mode="r", encoding="utf-8") as csvf:
        csv_reader = csv.DictReader(csvf)
        for rows in csv_reader:
            if rows.get("services"):
                rows["services"] = rows["services"].split(";")
            csv_data.append(smodel(**rows).model_dump(exclude_none=True))

    model_dao = dao[model]
    for data in csv_data:
        await model_dao.add(**data)
