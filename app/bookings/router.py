from datetime import date

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi import APIRouter, Depends

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



