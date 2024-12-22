from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from sqladmin import ModelView


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.booking]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Польователь"
    name_plural = "Польователи"
    icon = "fa-solid fa-user"

class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user, Bookings.room]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-calendar"

class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.booking]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"

class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"