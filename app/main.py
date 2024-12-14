from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.bookings.router import router as booking_router
from app.users.router import router as users_router
from app.pages.router import router as router_pages
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(users_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(images_router)


app.include_router(router_pages)
