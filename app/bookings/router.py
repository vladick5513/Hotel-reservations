from datetime import date

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi import APIRouter, Depends
from pydantic.v1 import parse_obj_as

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.get("")
async def get_bookings(
        room_id:int,
        date_from:date,
        date_to:date,
        user: Users = Depends(get_current_user)
) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
async def add_bookings(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    if not booking:
        raise RoomCannotBeBooked


    booking_dict = {
        "id": booking.id,
        "room_id": booking.room_id,
        "user_id": booking.user_id,
        "date_from": booking.date_from,
        "date_to": booking.date_to,
        "price": booking.price,
        "total_cost": booking.total_cost,
        "total_days": booking.total_days,
    }

    booking_pydantic = SBooking.model_validate(booking_dict)
    send_booking_confirmation_email.delay(booking_pydantic.model_dump(), user.email)

    return booking_pydantic.model_dump()


