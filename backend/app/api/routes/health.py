from fastapi import APIRouter
from app.db.session import check_database_connection

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint reporting overall backend service status and PostgreSQL connectivity.
    """
    is_connected, _ = check_database_connection()

    return {
        "status": "healthy" if is_connected else "degraded",
        "service": "CareerIQ Backend",
        "database": "connected" if is_connected else "disconnected",
    }
