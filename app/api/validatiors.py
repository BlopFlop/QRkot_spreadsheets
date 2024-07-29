from http import HTTPStatus

from fastapi import HTTPException

from app.models import CharityProject
from app.repository import RepositoryBase
from app.schemas import CharityProjectSchemaUpdate


async def check_name_duplicate(
    project_name: str, repository_project: RepositoryBase
) -> None:
    """Check duplicate name project in DB."""
    project = await repository_project.get_obj_for_field_arg(
        field="name", arg=project_name, many=False
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


def check_full_invested_project(project: CharityProject) -> None:
    """Check full invested project in DB."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект нельзя редактировать он полностью проинвестирован.",
        )


def check_has_deleted_project(project: CharityProject) -> None:
    """Check has deleted project in DB."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект нельзя удалить, средства уже внесены.",
        )


def check_full_amount_project(
    project: CharityProject, project_update: CharityProjectSchemaUpdate
) -> None:
    """Check new full_amount more than invested_amount."""
    invested_amount = project.invested_amount
    new_full_amount = project_update.full_amount
    if new_full_amount is not None:
        if new_full_amount < invested_amount:
            raise HTTPException(
                status_code=400,
                detail=(
                    "При редактировании проекта запрещено устанавливать"
                    " требуемую сумму меньше внесённой"
                ),
            )
