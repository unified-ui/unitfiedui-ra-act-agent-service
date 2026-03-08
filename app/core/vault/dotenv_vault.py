"""DotEnv vault implementation for local development."""

import os
import threading

from dotenv import load_dotenv

from app.core.vault.base import BaseVault


class DotEnvVault(BaseVault):
    """Vault implementation using environment variables and in-memory store."""

    def __init__(self) -> None:
        """Initialize the DotEnv vault."""
        load_dotenv(override=False)
        self._store: dict[str, str] = {}
        self._lock = threading.RLock()

    def get_secret(self, key: str) -> str | None:
        """Retrieve a secret from environment or in-memory store.

        Args:
            key: The secret key.

        Returns:
            The secret value, or None if not found.
        """
        env_value = os.getenv(key)
        if env_value:
            return env_value

        with self._lock:
            return self._store.get(key)

    def store_secret(self, key: str, value: str) -> str:
        """Store a secret in memory.

        Args:
            key: The secret key.
            value: The secret value.

        Returns:
            URI of the stored secret.
        """
        with self._lock:
            self._store[key] = value
        return f"dotenv://{key}"

    def ping(self) -> bool:
        """Check vault connectivity.

        Returns:
            Always True for DotEnv vault.
        """
        return True

    def close(self) -> None:
        """Close vault connections (no-op for DotEnv)."""
