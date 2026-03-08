"""Vault integration package."""

from app.core.vault.base import BaseVault
from app.core.vault.dependencies import get_app_vault
from app.core.vault.factory import create_vault

__all__ = ["BaseVault", "create_vault", "get_app_vault"]
