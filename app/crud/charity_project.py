from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectSchemaUpdate, CharityProjectSchemaCreate


class CRUDProject(CRUDBase):
    """CharityProject CRUD operations in current application."""

    async def update(
            self,
            charity_project_db: CharityProject,
            obj_in: CharityProjectSchemaUpdate,
            session: AsyncSession,
    ):
        """Update CharityProject item."""
        obj_data: dict[str: Any] = jsonable_encoder(charity_project_db)
        update_data = obj_in.dict(exclude_unset=True)

        new_full_amount = obj_in.full_amount
        invested_amount = charity_project_db.invested_amount

        if new_full_amount:
            if new_full_amount < invested_amount:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        'При редактировании проекта запрещено устанавливать'
                        ' требуемую сумму меньше внесённой'
                    )
                )
            elif new_full_amount == invested_amount:
                charity_project_db.fully_invested = True

        for field in obj_data:
            if field in update_data:
                setattr(charity_project_db, field, update_data[field])

        session.add(charity_project_db)
        await session.commit()
        await session.refresh(charity_project_db)
        return charity_project_db

    async def create(
            self,
            obj_in: CharityProjectSchemaCreate,
            session: AsyncSession,
    ):
        """Create project item."""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return db_obj

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> CharityProject:
        """Get id CharityProject for name."""
        project_id: Any = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        project_id = project_id.scalars().first()
        return project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:

        charity_project = await session.execute(
            select(
                CharityProject
            ).where(
                CharityProject.fully_invested
            ).order_by((
                extract('DAY', CharityProject.close_date) -
                extract('DAY', CharityProject.create_date)
            ))
        )
        return charity_project.scalars().all()


crud_project: CRUDProject = CRUDProject(CharityProject)
