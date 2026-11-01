"""Routers package."""
from app.api.v1.routers.health import router as health_router
from app.api.v1.routers.dashboard import router as dashboard_router
from app.api.v1.routers.literature import router as literature_router
from app.api.v1.routers.proteins import router as proteins_router
from app.api.v1.routers.biology import router as biology_router
from app.api.v1.routers.evidence import router as evidence_router
from app.api.v1.routers.research import router as research_router
from app.api.v1.routers.projects import router as projects_router
from app.api.v1.routers.reports import router as reports_router
from app.api.v1.routers.settings import router as settings_router
