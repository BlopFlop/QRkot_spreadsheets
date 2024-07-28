from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.repository import repository_donate
from app.models import User
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
    session: AsyncSession = Depends(get_async_session),
):
    return await repository_donate.get_multi(session=session)


@router.post(
    "/",
    response_model=DonationSchemmaDB,
    summary="Сделать пожертвование",
    description=(
        "Сделать пожертвование, которое распределится"
        " по всем свободным проектам."
    ),
)
async def create_donate(
    donation: DonationSchemmaCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    donation.__dict__["user_id"] = user.id
    donation = await repository_donate.create(donation, session)
    donation = await invest_process(donation, session)
    return donation


@router.get(
    "/my",
    response_model=list[DonationSchemmaDB],
    summary="Получить мои донаты",
    description="Получает все мои пожертвования из базы данных.",
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await repository_donate.get_obj_for_filed_arg(
        filed='user_id', arg=user.id, many=True, session=session
    )
