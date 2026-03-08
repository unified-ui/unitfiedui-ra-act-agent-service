"""Vault dependency injection."""

import functools

from app.config import settings
from app.core.vault.base import BaseVault
from app.core.vault.factory import create_vault


@functools.cache
def get_app_vault() -> BaseVault:
    """Get the application vault singleton for S2S key resolution.

    Returns:
        A vault instance configured for application secrets.
    """
    vault_type = settings.effective_app_vault_type
    return create_vault(
        vault_type=vault_type,
        vault_url=settings.azure_keyvault_url,
        addr=settings.hashicorp_vault_addr,
        token=settings.hashicorp_vault_token,
        mount_point=settings.hashicorp_vault_mount_point,
    )
