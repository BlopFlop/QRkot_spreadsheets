from app.api.endpoints.charity_project import router as project_router
from app.api.endpoints.donation import router as donat_router
from app.api.endpoints.google_api import router as google_router
from app.api.endpoints.user import router as user_router

__all__ = ["donat_router", "project_router", "user_router", "google_router"]
