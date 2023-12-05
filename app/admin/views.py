from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    name = "User"
    name_plural = "Users"
    column_list = [Users.id, Users.email, Users.bookings]
    form_excluded_columns = [Users.hashed_password]
    can_delete = False
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    name = "Booking"
    name_plural = "Bookings"
    column_list = "__all__"
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    name = "Hotel"
    name_plural = "Hotels"
    column_list = "__all__"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    name = "Room"
    name_plural = "Rooms"
    column_list = "__all__"
    icon = "fa-solid fa-bed"
