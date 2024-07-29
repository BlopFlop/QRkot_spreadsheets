from fastapi import APIRouter, Depends

from app.core.user import current_superuser, current_user
from app.models import User
from app.repository import (
    RepositoryBase,
    get_repository_donation,
    get_repository_project,
)
from app.schemas import (
    AllDonationsSchemaDB,
    DonationSchemmaCreate,
    DonationSchemmaDB,
)
from app.services import invest_process

router = APIRouter()


@router.get(
    "/",
    response_model=list[AllDonationsSchemaDB],
    dependencies=[Depends(current_superuser)],
    summary="Получить все донаты",
    description="Получает все пожертвования из базы данных.",
)
async def get_all_donations(
    repository_donation=Depends(get_repository_donation),
):
    return await repository_donation.get_multi()


@router.post(
    "/",
    response_model=DonationSchemmaDB,
    summary="Сделать пожертвование",
    description=(
        "Сделать пожертвование, которое распределится"
        " по всем свободным проектам."
    ),
)
async def create_donation(
    donation: DonationSchemmaCreate,
    user: User = Depends(current_user),
    repository_donation: RepositoryBase = Depends(get_repository_donation),
    repository_project: RepositoryBase = Depends(get_repository_project),
):
    donation.__dict__["user_id"] = user.id
    donation = await repository_donation.create(donation)
    donation = await invest_process(
        new_obj=donation, repository=repository_project
    )
    return donation


@router.get(
    "/my",
    response_model=list[DonationSchemmaDB],
    summary="Получить мои донаты",
    description="Получает все мои пожертвования из базы данных.",
)
async def get_user_donations(
    user: User = Depends(current_user),
    repository_donation: RepositoryBase = Depends(get_repository_donation),
):
    return await repository_donation.get_obj_for_field_arg(
        field="user_id", arg=user.id, many=True
    )
