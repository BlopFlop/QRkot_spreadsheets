from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas import DonationSchemmaCreate


class CRUDDonate(CRUDBase):

    async def create(
            self,
            obj_in: DonationSchemmaCreate,
            user_id: int,
            session: AsyncSession,
    ):
        """Create donate model."""
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user_id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return db_obj

    async def get_donation_for_user_id(
            self,
            user_id: int,
            session: AsyncSession
    ):
        """Get donation for user id."""
        user_donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user_id
            )
        )
        return user_donations.scalars().all()


crud_donate: CRUDDonate = CRUDDonate(Donation)
