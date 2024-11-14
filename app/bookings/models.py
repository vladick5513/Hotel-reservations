import datetime
from sqlalchemy import Date, ForeignKey, Integer, Computed
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column( primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[datetime.date] = mapped_column(nullable=False)
    date_to: Mapped[datetime.date] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))