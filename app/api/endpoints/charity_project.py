from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validatiors import (
    check_full_amount_project,
    check_full_invested_project,
    check_has_deleted_project,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import CharityProject
from app.repository import repository_project
from app.schemas import (
    CharityProjectSchemaCreate,
    CharityProjectSchemaDB,
    CharityProjectSchemaUpdate,
)
from app.services import invest_process

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectSchemaDB],
    summary="Получить все проекты",
    description="Получает проекты из базы данных.",
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> list[CharityProject]:
    return await repository_project.get_multi(session=session)


@router.post(
    "/",
    response_model=CharityProjectSchemaDB,
    dependencies=[Depends(current_superuser)],
    summary="Создать проект.",
    description="Создает проект и сразу запускает процесс инвестирования.",
)
async def create_charity_project(
    charity_project: CharityProjectSchemaCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    await check_name_duplicate(
        project_name=charity_project.name, session=session
    )
    new_project = await repository_project.create(
        obj_in=charity_project, session=session
    )
    new_project = await invest_process(new_project, session)
    return new_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectSchemaDB,
    dependencies=[Depends(current_superuser)],
    summary="Удалить проект.",
    description=(
        "Удаляет проект(* удаление уже проинвестированного "
        "проекта невозможно)."
    ),
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    project = await repository_project.get(obj_id=project_id, session=session)
    check_has_deleted_project(project)
    return await repository_project.remove(db_obj=project, session=session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectSchemaDB,
    dependencies=[Depends(current_superuser)],
    summary="Изменить проект.",
)
async def change_charity_project(
    project_id: int,
    obj_in: CharityProjectSchemaUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    project_name = obj_in.name

    if project_name:
        await check_name_duplicate(obj_in.name, session)

    project = await repository_project.get(obj_id=project_id, session=session)

    check_full_invested_project(project)
    check_full_amount_project(project, obj_in)

    return await repository_project.update(project, obj_in, session)
