"""
Health, system status, and storage endpoints.
"""

import shutil
from pathlib import Path
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.core.config import get_settings

router = APIRouter(tags=["Health & System"])


@router.get("/health")
async def health_check():
    """Basic service health check."""
    return {
        "status": "healthy",
        "service": "ARAKNO-AI Backend",
        "version": get_settings().app_version,
    }


@router.get("/system/status")
async def system_status(db: AsyncSession = Depends(get_db)):
    """System diagnostics, database connectivity, and configuration status."""
    db_ok = False
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    settings = get_settings()

    return {
        "database_connected": db_ok,
        "database_url": settings.database_url.split("@")[-1],  # Safe URL without credentials
        "data_directory": str(Path(settings.data_dir).resolve()),
        "privacy_mode": settings.privacy_mode,
        "llm_provider": settings.llm_provider,
        "ncbi_email_configured": bool(settings.ncbi_email),
        "host": settings.host,
        "port": settings.port,
    }


@router.get("/system/storage")
async def system_storage():
    """Disk space and storage directory usage statistics."""
    settings = get_settings()
    data_path = Path(settings.data_dir).resolve()

    total, used, free = shutil.disk_usage(data_path if data_path.exists() else ".")

    # Calculate size of storage directories
    def dir_size(p: Path) -> int:
        if not p.exists():
            return 0
        return sum(f.stat().st_size for f in p.glob("**/*") if f.is_file())

    structures_size = dir_size(Path(settings.structures_dir))
    reports_size = dir_size(Path(settings.reports_dir))

    return {
        "disk_total_gb": round(total / (1024**3), 2),
        "disk_used_gb": round(used / (1024**3), 2),
        "disk_free_gb": round(free / (1024**3), 2),
        "structures_size_mb": round(structures_size / (1024**2), 2),
        "reports_size_mb": round(reports_size / (1024**2), 2),
    }
