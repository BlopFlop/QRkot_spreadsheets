from fastapi import FastAPI

from app.api import router
from app.core.config import settings, configure_logging
from app.core.init_db import create_first_superuser

configure_logging()

app = FastAPI(title=settings.app_title)

app.include_router(router)


@app.on_event("startup")
async def startup() -> None:
    """Start work FastApi project."""
    await create_first_superuser()
