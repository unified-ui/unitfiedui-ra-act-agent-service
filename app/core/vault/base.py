"""Abstract base class for vault implementations."""

from abc import ABC, abstractmethod


class BaseVault(ABC):
    """Abstract base class for secret vault implementations."""

    @abstractmethod
    def get_secret(self, key: str) -> str | None:
        """Retrieve a secret by key.

        Args:
            key: The secret key to retrieve.

        Returns:
            The secret value, or None if not found.
        """

    @abstractmethod
    def store_secret(self, key: str, value: str) -> str:
        """Store a secret.

        Args:
            key: The secret key.
            value: The secret value.

        Returns:
            URI of the stored secret.
        """

    @abstractmethod
    def ping(self) -> bool:
        """Check vault connectivity.

        Returns:
            True if the vault is reachable.
        """

    @abstractmethod
    def close(self) -> None:
        """Close vault connections."""
