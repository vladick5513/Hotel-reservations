from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from fastapi import APIRouter

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.get("")
async def get_bookings() -> list[SBooking]:
    return await BookingDAO.find_all()



