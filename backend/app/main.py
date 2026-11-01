"""
ARAKNO-AI FastAPI Main Application Entry Point.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.logging import get_logger
from app.db.database import init_db, close_db

# Import all routers
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

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle management."""
    settings = get_settings()
    settings.ensure_directories()
    logger.info("Initializing ARAKNO-AI database...")
    await init_db()
    logger.info("Database and research divisions ready.")
    yield
    logger.info("Shutting down ARAKNO-AI backend...")
    await close_db()


def create_application() -> FastAPI:
    """Factory creating and configuring the FastAPI app."""
    settings = get_settings()

    app = FastAPI(
        title="ARAKNO-AI API",
        description=(
            "Advanced Research and Knowledge Architecture for Novel Organism-inspired Biomedical Research. "
            "Local-first computational biology and scientific intelligence platform."
        ),
        version=settings.app_version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Restrict CORS to localhost only
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API v1 routers
    api_prefix = "/api/v1"
    app.include_router(health_router, prefix=api_prefix)
    app.include_router(dashboard_router, prefix=api_prefix)
    app.include_router(literature_router, prefix=api_prefix)
    app.include_router(proteins_router, prefix=api_prefix)
    app.include_router(biology_router, prefix=api_prefix)
    app.include_router(evidence_router, prefix=api_prefix)
    app.include_router(research_router, prefix=api_prefix)
    app.include_router(projects_router, prefix=api_prefix)
    app.include_router(reports_router, prefix=api_prefix)
    app.include_router(settings_router, prefix=api_prefix)

    @app.get("/")
    async def root():
        return {
            "name": "ARAKNO-AI",
            "version": settings.app_version,
            "status": "online",
            "documentation": "/docs",
            "api_prefix": api_prefix,
        }

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
