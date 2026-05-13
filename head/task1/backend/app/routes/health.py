"""
LogPulse Mini SIEM - Health Route
Provides a simple health check endpoint for monitoring.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns status and current server timestamp.
    Used by Docker HEALTHCHECK and monitoring tools.
    """
    return {
        "status": "ok",
        "service": "LogPulse Mini SIEM",
        "timestamp": datetime.utcnow().isoformat(),
    }
