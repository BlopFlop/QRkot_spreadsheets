from fastapi import Depends

from app.core.db import get_async_session
from app.models import CharityProject
from app.repository.base import RepositoryBase


async def get_repository_project(
    session=Depends(get_async_session),
) -> RepositoryBase:
    return RepositoryBase(CharityProject, session=session)


