"""FastAPI application factory."""

import logging

from fastapi import FastAPI

from app.api.v1.agent import router as agent_router
from app.api.v1.health import router as health_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    application = FastAPI(
        title="unified-ui ReACT Agent Service",
        description="ReACT Agent execution service for the unified-ui platform",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.include_router(health_router)
    application.include_router(agent_router, prefix="/api/v1")

    return application


app = create_app()
