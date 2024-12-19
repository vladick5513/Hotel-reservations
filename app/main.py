from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from app.admin.views import UsersAdmin
from app.config import settings
from app.database import async_engine
from app.users.models import Users
from fastapi import FastAPI
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


admin = Admin(app, async_engine)

admin.add_view(UsersAdmin)
