"""
Health check endpoints for the AI Chat Bot backend.

This module provides health check endpoints to monitor the application's status,
database connectivity, and external service availability.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .db import get_db_session
from .config import settings

router = APIRouter(prefix="/health", tags=["health"])

# Configure logger for health checks
logger = logging.getLogger(__name__)


@router.get("/", response_model=Dict[str, Any])
def health_check():
    """
    Main health check endpoint that returns the overall application status.

    Returns:
        Dict containing status information including:
        - status: Overall health status
        - timestamp: When the check was performed
        - uptime: Application uptime
        - version: Application version
        - services: Status of dependent services
    """
    try:
        # Check database connectivity
        db_status = check_database_health()

        # For Phase 3, we consider the app healthy if the database is connected
        # We don't require external services like OpenAI for core functionality
        health_response = {
            "status": "ok" if db_status["status"] == "connected" else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": "unknown",  # This would typically come from a global app start time
            "version": "1.0.0",  # This should come from your versioning system
            "services": {
                "database": db_status,
            }
        }

        logger.info(f"Health check completed with status: {health_response['status']}")
        return health_response

    except Exception as e:
        logger.error(f"Health check failed with error: {str(e)}")
        raise HTTPException(status_code=503, detail={
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })


@router.get("/database", response_model=Dict[str, Any])
def database_health():
    """
    Specific health check for database connectivity.

    Returns:
        Dict containing database connection status and details
    """
    try:
        db_status = check_database_health()
        return db_status
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail={
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })


@router.get("/api-status", response_model=Dict[str, Any])
def api_status():
    """
    Check the status of external APIs used by the application.

    Returns:
        Dict containing status of external services
    """
    # For Phase 3, we don't require external APIs to be working for core functionality
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "openai": {
                "status": "not_required_for_core",
                "message": "OpenAI API not required for core Phase 3 functionality",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    }


def check_database_health() -> Dict[str, Any]:
    """
    Check the health of the database connection.

    Returns:
        Dict containing database health information
    """
    try:
        from .db import get_db_session
        # Attempt to get a database session and run a simple query
        with get_db_session() as session:
            # Run a simple query to test connectivity
            result = session.exec(text("SELECT 1"))
            _ = result.one_or_none()

            return {
                "status": "connected",
                "message": "Successfully connected to database",
                "timestamp": datetime.utcnow().isoformat(),
                "database_type": "sqlite",  # This could be dynamic based on config
            }
    except SQLAlchemyError as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "disconnected",
            "error": f"Database connection failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Unexpected error during database health check: {str(e)}")
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }


async def check_external_services() -> Dict[str, Any]:
    """
    Check the status of external services like OpenAI API.

    Returns:
        Dict containing status of external services
    """
    external_checks = {}

    # Check OpenAI API connectivity
    try:
        import httpx
        import os

        openai_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if not openai_key:
            external_checks["openai"] = {
                "status": "missing_config",
                "message": "OpenAI API key not configured",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            # Make a lightweight request to check API accessibility
            headers = {
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json"
            }

            async with httpx.AsyncClient(timeout=5.0) as client:
                # Use a minimal request to test connectivity
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    headers=headers
                )

                if response.status_code == 200:
                    external_checks["openai"] = {
                        "status": "reachable",
                        "message": "OpenAI API is accessible",
                        "timestamp": datetime.utcnow().isoformat(),
                        "response_time_ms": response.elapsed.total_seconds() * 1000
                    }
                else:
                    external_checks["openai"] = {
                        "status": "unreachable",
                        "message": f"OpenAI API returned status {response.status_code}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
    except httpx.ConnectTimeout:
        logger.warning("OpenAI API health check timed out")
        external_checks["openai"] = {
            "status": "timeout",
            "message": "OpenAI API request timed out",
            "timestamp": datetime.utcnow().isoformat()
        }
    except httpx.RequestError as e:
        logger.error(f"OpenAI API health check failed: {str(e)}")
        external_checks["openai"] = {
            "status": "error",
            "message": f"OpenAI API request failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Unexpected error during OpenAI API health check: {str(e)}")
        external_checks["openai"] = {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }

    return external_checks


@router.get("/ready", response_model=Dict[str, Any])
def readiness_check():
    """
    Readiness check to determine if the application is ready to serve traffic.

    This endpoint checks if all critical dependencies are available.

    Returns:
        Dict containing readiness status
    """
    try:
        # For readiness, we primarily check if the database is available
        db_status = check_database_health()

        is_ready = db_status["status"] == "connected"

        readiness_response = {
            "ready": is_ready,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "database": db_status
            }
        }

        if not is_ready:
            raise HTTPException(status_code=503, detail=readiness_response)

        logger.debug("Readiness check passed")
        return readiness_response

    except HTTPException:
        # Re-raise HTTP exceptions (like 503 from readiness failure)
        raise
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(status_code=503, detail={
            "ready": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })