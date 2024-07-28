from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.repository.charity_project import repository_project
from app.services.google_api import (
    create_spreadsheet,
    set_user_permissions_in_spreadsheet,
    update_spreadsheet,
)

router = APIRouter()


@router.post(
    "/",
    response_model=list[dict[str, int]],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    charity_projects = await repository_project.get_obj_for_filed_arg(
        "fully_invested", True, session
    )

    spreadsheetid = await create_spreadsheet(wrapper_services)
    await set_user_permissions_in_spreadsheet(spreadsheetid, wrapper_services)
    await update_spreadsheet(spreadsheetid, charity_projects, wrapper_services)
    return charity_projects
