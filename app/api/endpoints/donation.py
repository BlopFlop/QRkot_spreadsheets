from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import crud_donate
from app.models import Donation, User
from app.schemas import (
    AllDonationsSchemaDB, DonationSchemmaDB, DonationSchemmaCreate
)
from app.services import invest_process


router = APIRouter()


@router.get(
    '/',
    response_model=list[AllDonationsSchemaDB],
    dependencies=[Depends(current_superuser)],
    summary='Получить все донаты',
    description='Получает все пожертвования из базы данных.'
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    donations: list[Donation] = await crud_donate.get_multi(session=session)
    return donations


@router.post(
    '/',
    response_model=DonationSchemmaDB,
    summary='Сделать пожертвование',
    description=(
        'Сделать пожертвование, которое распределится'
        ' по всем свободным проектам.'
    )
)
async def create_charity_project(
        donation: DonationSchemmaCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    donation: list[Donation] = await crud_donate.create(
        obj_in=donation,
        user_id=user.id,
        session=session
    )
    await invest_process(donation, session)
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/my',
    response_model=list[DonationSchemmaDB],
    summary='Получить мои донаты',
    description='Получает все мои пожертвования из базы данных.'
)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_donations: list[Donation] = (
        await crud_donate.get_donation_for_user_id(
            user_id=user.id,
            session=session
        )
    )
    return user_donations
