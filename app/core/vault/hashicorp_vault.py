"""HashiCorp Vault implementation."""

import logging

import hvac

from app.core.vault.base import BaseVault

logger = logging.getLogger(__name__)


class HashiCorpVault(BaseVault):
    """Vault implementation using HashiCorp Vault."""

    def __init__(self, addr: str, token: str, mount_point: str = "secret") -> None:
        """Initialize HashiCorp Vault client.

        Args:
            addr: Vault server address.
            token: Authentication token.
            mount_point: KV v2 mount point.
        """
        self._client = hvac.Client(url=addr, token=token)
        self._mount_point = mount_point

        if not self._client.is_authenticated():
            msg = "HashiCorp Vault authentication failed"
            raise ConnectionError(msg)

    def get_secret(self, key: str) -> str | None:
        """Retrieve a secret from HashiCorp Vault.

        Args:
            key: The secret key.

        Returns:
            The secret value, or None if not found.
        """
        try:
            result = self._client.secrets.kv.v2.read_secret_version(
                path=key,
                mount_point=self._mount_point,
            )
            data = result.get("data", {}).get("data", {})
            return data.get("value")  # type: ignore[no-any-return]
        except Exception:
            logger.warning("Failed to get secret '%s' from HashiCorp Vault", key)
            return None

    def store_secret(self, key: str, value: str) -> str:
        """Store a secret in HashiCorp Vault.

        Args:
            key: The secret key.
            value: The secret value.

        Returns:
            URI of the stored secret.
        """
        self._client.secrets.kv.v2.create_or_update_secret(
            path=key,
            secret={"value": value},
            mount_point=self._mount_point,
        )
        host = self._client.url or "localhost"
        return f"vault://{host}/{self._mount_point}/{key}"

    def ping(self) -> bool:
        """Check HashiCorp Vault connectivity.

        Returns:
            True if the vault is reachable and authenticated.
        """
        try:
            return bool(self._client.is_authenticated())
        except Exception:
            return False

    def close(self) -> None:
        """Close HashiCorp Vault client (no-op)."""
