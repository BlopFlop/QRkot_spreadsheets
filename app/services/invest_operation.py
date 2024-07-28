from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_full_invest(
    model: Union[CharityProject, Donation], session: AsyncSession
) -> list[Union[CharityProject, Donation]]:
    """Get model item for not full invested."""
    not_full_invest = await session.execute(
        select(model).where(model.fully_invested == 0)
    )
    objs = not_full_invest.scalars().all()

    if objs is None:
        return []
    return objs


def close_obj(obj: Union[CharityProject, Donation]):
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.utcnow()
    return obj


def fill_obj(
    new_obj: Union[CharityProject, Donation],
    db_obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    remainder_amount_new_obj = new_obj.full_amount - new_obj.invested_amount
    remainder_amount_db_item = db_obj.full_amount - db_obj.invested_amount

    if remainder_amount_new_obj > remainder_amount_db_item:
        new_obj.invested_amount += remainder_amount_db_item
        close_obj(db_obj)

    elif remainder_amount_new_obj < remainder_amount_db_item:
        db_obj.invested_amount += remainder_amount_new_obj
        close_obj(new_obj)

    else:
        close_obj(new_obj)
        close_obj(db_obj)

    session.add(new_obj)
    session.add(db_obj)


async def invest_process(
    new_obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    if isinstance(new_obj, CharityProject):
        no_full_invest_objs: Donation = await get_not_full_invest(
            Donation, session
        )
    else:
        no_full_invest_objs: CharityProject = await get_not_full_invest(
            CharityProject, session
        )

    for model in no_full_invest_objs:
        fill_obj(new_obj, model, session)

    await session.commit()
    await session.refresh(new_obj)
    return new_obj
