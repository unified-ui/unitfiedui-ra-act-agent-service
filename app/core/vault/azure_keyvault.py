"""Azure Key Vault implementation."""

import logging

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from app.core.vault.base import BaseVault

logger = logging.getLogger(__name__)


class AzureKeyVault(BaseVault):
    """Vault implementation using Azure Key Vault."""

    def __init__(self, vault_url: str) -> None:
        """Initialize Azure Key Vault client.

        Args:
            vault_url: The URL of the Azure Key Vault.
        """
        credential = DefaultAzureCredential()
        self._client = SecretClient(vault_url=vault_url, credential=credential)
        self._vault_name = vault_url.split("//")[1].split(".")[0] if "//" in vault_url else vault_url

    @staticmethod
    def _sanitize_key(key: str) -> str:
        """Sanitize key for Azure Key Vault compatibility.

        Args:
            key: The original key.

        Returns:
            Sanitized key with underscores and dots replaced by hyphens.
        """
        return key.replace("_", "-").replace(".", "-")

    def get_secret(self, key: str) -> str | None:
        """Retrieve a secret from Azure Key Vault.

        Args:
            key: The secret key.

        Returns:
            The secret value, or None if not found.
        """
        try:
            secret = self._client.get_secret(self._sanitize_key(key))
            return secret.value
        except Exception:
            logger.warning("Failed to get secret '%s' from Azure Key Vault", key)
            return None

    def store_secret(self, key: str, value: str) -> str:
        """Store a secret in Azure Key Vault.

        Args:
            key: The secret key.
            value: The secret value.

        Returns:
            URI of the stored secret.
        """
        sanitized = self._sanitize_key(key)
        result = self._client.set_secret(sanitized, value)
        version = result.properties.version or "latest"
        return f"azurekv://{self._vault_name}/{sanitized}/{version}"

    def ping(self) -> bool:
        """Check Azure Key Vault connectivity.

        Returns:
            True if the vault is reachable.
        """
        try:
            next(self._client.list_properties_of_secrets(max_page_size=1), None)
            return True
        except Exception:
            logger.warning("Azure Key Vault ping failed")
            return False

    def close(self) -> None:
        """Close Azure Key Vault client."""
        self._client.close()
