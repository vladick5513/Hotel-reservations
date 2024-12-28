from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import time

from app.admin.auth import authentication_backend
from app.admin.views import UsersAdmin, BookingsAdmin, RoomsAdmin, HotelsAdmin
from app.config import settings
from app.database import async_engine
from app.users.models import Users
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.bookings.router import router as booking_router
from app.users.router import router as users_router
from app.pages.router import router as router_pages
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin, ModelView
from redis import asyncio as aioredis
from app.logger import logger

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(users_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(images_router)
app.include_router(router_pages)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie","Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin","Authorization"],
)


admin = Admin(app, async_engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response