from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


if settings.MODE == "TEST":
    DATABASE_URL_asyncpg = settings.TEST_DATABASE_URL_asyncpg
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL_asyncpg = settings.DATABASE_URL_asyncpg
    DATABASE_PARAMS = {}

async_engine = create_async_engine(DATABASE_URL_asyncpg, **DATABASE_PARAMS)


async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass