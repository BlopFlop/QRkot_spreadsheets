from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_full_invest(
        model: Union[CharityProject, Donation],
        session: AsyncSession
) -> Union[CharityProject, Donation]:
    """Get model item for not full invested."""
    not_full_invest = await session.execute(
        select(model).where(model.fully_invested == 0)
    )
    result_list: list[CharityProject, Donation] = (
        not_full_invest.scalars().all()
    )
    if result_list is None:
        return []
    return result_list


def get_invested_amount(model: Union[CharityProject, Donation]) -> int:
    if model.invested_amount is None:
        return 0
    return model.invested_amount


async def invest_process(
        create_item: Union[CharityProject, Donation],
        session: AsyncSession
) -> list[CharityProject, Donation]:
    """Start invest process in project."""
    projects: list[CharityProject] = await get_not_full_invest(
        CharityProject,
        session
    )
    donation: list[Donation] = await get_not_full_invest(
        Donation,
        session
    )
    if isinstance(create_item, CharityProject):
        projects.append(create_item)
    elif isinstance(create_item, Donation):
        donation.append(create_item)

    index_project: int = 0
    len_projects: int = len(projects) - 1
    index_donate: int = 0
    len_donations: int = len(donation) - 1

    while (index_project <= len_projects) and (index_donate <= len_donations):
        project: CharityProject = projects[index_project]
        donat: Donation = donation[index_donate]

        remainder_amount_project: int = (
            project.full_amount - get_invested_amount(project)
        )
        remainder_amount_donat: int = (
            donat.full_amount - get_invested_amount(donat)
        )
        if remainder_amount_project > remainder_amount_donat:
            project.invested_amount += remainder_amount_donat

            donat.invested_amount = donat.full_amount
            donat.fully_invested = True
            donat.close_date = datetime.utcnow()
            index_donate += 1

        elif remainder_amount_donat < remainder_amount_project:
            donat.invested_amount += remainder_amount_project

            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.utcnow()
            index_project += 1

        else:
            donat.invested_amount = donat.full_amount
            donat.fully_invested = True
            donat.close_date = datetime.utcnow()
            index_donate += 1
            project.invested_amount = project.full_amount
            project.fully_invested = True
            project.close_date = datetime.utcnow()
            index_project += 1

        session.add(project)
        session.add(donat)
