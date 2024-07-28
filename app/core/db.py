from typing import Any, AsyncGenerator

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeMeta,
    declarative_base,
    declared_attr,
    sessionmaker,
)

from app.core.config import settings


class PreBase:
    """Class for add the same ones methods and properties."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base: DeclarativeMeta = declarative_base(cls=PreBase)

engine: AsyncEngine = create_async_engine(settings.database_url)

AsyncSessionLocal: sessionmaker = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[Any, AsyncSession]:
    """Generator session."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
