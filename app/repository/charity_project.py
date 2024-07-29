from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import CharityProject
from app.repository.base import RepositoryBase


async def get_repository_project(
    session: AsyncSession = Depends(get_async_session),
) -> RepositoryBase:
    return RepositoryBase(CharityProject, session=session)
