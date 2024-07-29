from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.repository.base import RepositoryBase


def close_obj(obj: Union[CharityProject, Donation]):
    """Close invest process in object."""
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.utcnow()
    return obj


def fill_obj(
    new_obj: Union[CharityProject, Donation],
    db_obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """Fill donation in project."""
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
    repository: RepositoryBase,
) -> Union[CharityProject, Donation]:
    """Start invest process in projects."""
    no_full_invest_objs = await repository.get_obj_for_field_arg(
        field="fully_invested", arg=False, many=True
    )

    for model in no_full_invest_objs:
        fill_obj(new_obj, model, repository.session)

    await repository.session.commit()
    await repository.session.refresh(new_obj)
    return new_obj
