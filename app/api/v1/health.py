"""Health check endpoints."""

from fastapi import APIRouter

from app.core.vault.dependencies import get_app_vault

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Return service health status.

    Returns:
        Health status response.
    """
    return {"status": "ok"}


@router.get("/ready")
async def ready() -> dict[str, str]:
    """Return service readiness status.

    Checks vault connectivity to verify the service is ready.

    Returns:
        Readiness status response.
    """
    vault = get_app_vault()
    is_ready = vault.ping()
    if not is_ready:
        return {"status": "not_ready", "detail": "Vault connection failed"}
    return {"status": "ready"}
