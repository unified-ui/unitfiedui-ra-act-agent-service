"""Tests for vault implementations."""

import os

import pytest
from app.core.vault.dotenv_vault import DotEnvVault
from app.core.vault.factory import create_vault


@pytest.mark.unit
class TestDotEnvVault:
    """Tests for the DotEnvVault implementation."""

    def test_store_and_get_secret(self) -> None:
        """Test storing and retrieving a secret."""
        vault = DotEnvVault()
        uri = vault.store_secret("test_key", "test_value")
        assert uri == "dotenv://test_key"
        assert vault.get_secret("test_key") == "test_value"

    def test_get_secret_from_env(self) -> None:
        """Test retrieving a secret from environment variable."""
        os.environ["TEST_ENV_SECRET"] = "env_value"
        vault = DotEnvVault()
        assert vault.get_secret("TEST_ENV_SECRET") == "env_value"
        del os.environ["TEST_ENV_SECRET"]

    def test_get_nonexistent_secret_returns_none(self) -> None:
        """Test that getting a nonexistent secret returns None."""
        vault = DotEnvVault()
        assert vault.get_secret("nonexistent_key_xyz") is None

    def test_ping_returns_true(self) -> None:
        """Test that ping always returns True."""
        vault = DotEnvVault()
        assert vault.ping() is True

    def test_close_is_noop(self) -> None:
        """Test that close is a no-op."""
        vault = DotEnvVault()
        vault.close()


@pytest.mark.unit
class TestVaultFactory:
    """Tests for the vault factory."""

    def test_create_dotenv_vault(self) -> None:
        """Test creating a DotEnv vault."""
        vault = create_vault("dotenv")
        assert isinstance(vault, DotEnvVault)

    def test_create_dotenv_vault_case_insensitive(self) -> None:
        """Test that vault type is case-insensitive."""
        vault = create_vault("DOTENV")
        assert isinstance(vault, DotEnvVault)

    def test_create_unsupported_vault_raises_error(self) -> None:
        """Test that unsupported vault type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported vault type"):
            create_vault("unsupported")

    def test_azure_keyvault_requires_url(self) -> None:
        """Test that Azure Key Vault requires a URL."""
        with pytest.raises(ValueError, match="Azure Key Vault URL is required"):
            create_vault("azure_keyvault")
