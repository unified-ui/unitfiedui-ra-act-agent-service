"""Service-to-service authentication middleware."""

import logging

from fastapi import Header, HTTPException

from app.config import settings
from app.core.vault.dependencies import get_app_vault

logger = logging.getLogger(__name__)


async def validate_service_key(x_service_key: str = Header(...)) -> None:
    """Validate the service-to-service authentication key.

    Args:
        x_service_key: Service key from the X-Service-Key header.

    Raises:
        HTTPException: 401 if key is missing, 403 if key is invalid.
    """
    if not x_service_key:
        raise HTTPException(status_code=401, detail="Missing service key")

    vault = get_app_vault()
    expected_key = vault.get_secret(settings.app_vault_key_agent_to_react_service)

    if not expected_key:
        logger.error("Service key not configured in vault")
        raise HTTPException(status_code=500, detail="Service key not configured")

    if x_service_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid service key")
