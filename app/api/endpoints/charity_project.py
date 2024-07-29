from fastapi import APIRouter, Depends

from app.api.validatiors import (
    check_full_amount_project,
    check_full_invested_project,
    check_has_deleted_project,
    check_name_duplicate,
)
from app.core.user import current_superuser
from app.models import CharityProject
from app.repository import (
    RepositoryBase,
    get_repository_donation,
    get_repository_project,
)
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
    repository_project: RepositoryBase = Depends(get_repository_project),
) -> list[CharityProject]:
    return await repository_project.get_multi()


@router.post(
    "/",
    response_model=CharityProjectSchemaDB,
    dependencies=[Depends(current_superuser)],
    summary="Создать проект.",
    description="Создает проект и сразу запускает процесс инвестирования.",
)
async def create_charity_project(
    charity_project: CharityProjectSchemaCreate,
    repository_project: RepositoryBase = Depends(get_repository_project),
    repository_donation: RepositoryBase = Depends(get_repository_donation),
) -> CharityProject:
    await check_name_duplicate(
        project_name=charity_project.name,
        repository_project=repository_project,
    )
    new_project = await repository_project.create(obj_in=charity_project)
    new_project = await invest_process(
        new_obj=new_project,
        repository=repository_donation,
    )
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
    project_id: int,
    repository_project: RepositoryBase = Depends(get_repository_project),
) -> CharityProject:
    project = await repository_project.get(obj_id=project_id)
    check_has_deleted_project(project)
    return await repository_project.remove(db_obj=project)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectSchemaDB,
    dependencies=[Depends(current_superuser)],
    summary="Изменить проект.",
)
async def change_charity_project(
    project_id: int,
    obj_in: CharityProjectSchemaUpdate,
    repository_project: RepositoryBase = Depends(get_repository_project),
) -> CharityProject:
    project_name = obj_in.name

    if project_name:
        await check_name_duplicate(obj_in.name, repository_project)

    project = await repository_project.get(obj_id=project_id)

    check_full_invested_project(project)
    check_full_amount_project(project, obj_in)

    return await repository_project.update(project, obj_in)
