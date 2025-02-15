from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import DATE_FORMAT
from app.models import CharityProject


async def create_spreadsheet(wrapper_services: Aiogoogle) -> str:
    """Create table in google services."""
    now_date_time = datetime.now().strftime(DATE_FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheet_body = {
        "properties": {
            "title": f"Отчёт на {now_date_time}",
            "locale": "ru_RU",
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridProperties": {"rowCount": 100, "columnCount": 11},
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response["spreadsheetId"]
    return spreadsheetid


async def set_user_permissions_in_spreadsheet(
    spreadsheetid: str, wrapper_services: Aiogoogle
) -> None:
    """Get permission user for google tab."""
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields="id"
        )
    )


async def update_spreadsheet(
    spreadsheetid: str,
    charity_projects: list[CharityProject],
    wrapper_services: Aiogoogle,
) -> None:
    """Update data in tab."""
    now_date_time = datetime.now().strftime(DATE_FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    table_values = [
        ["Отчёт от", now_date_time],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]

    for charity_project in charity_projects:
        new_row = [
            charity_project.name,
            charity_project.close_date - charity_project.create_date,
            charity_project.description,
        ]
        table_values.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_values}

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range="A1:C30",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
