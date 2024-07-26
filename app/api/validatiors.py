from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_project
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Check duplicate name project in DB."""
    room_id = await crud_project.get_project_id_by_name(project_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


def check_full_invested_project(
        project: CharityProject
) -> None:
    """Check full invested project in DB."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект нельзя редактировать он полностью проинвестирован.'
        )


def check_has_deleted_project(
        project: CharityProject
) -> None:
    """Check has deleted project in DB."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект нельзя удалить, средства уже внесены.'
        )
