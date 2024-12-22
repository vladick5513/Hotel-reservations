import pytest

import os
os.environ["MODE"] = "TEST"

from app.database import async_engine, Base
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.main import app
from app.users.models import Users
from app.bookings.models import Bookings
from httpx import AsyncClient
from app.config import settings


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac