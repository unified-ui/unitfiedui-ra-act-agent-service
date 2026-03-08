"""Tests for vault implementations."""

import os
from unittest.mock import MagicMock, patch

import pytest
from app.core.vault.azure_keyvault import AzureKeyVault
from app.core.vault.dotenv_vault import DotEnvVault
from app.core.vault.factory import create_vault
from app.core.vault.hashicorp_vault import HashiCorpVault


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


@pytest.mark.unit
class TestAzureKeyVault:
    """Tests for the AzureKeyVault implementation."""

    @patch("app.core.vault.azure_keyvault.SecretClient")
    @patch("app.core.vault.azure_keyvault.DefaultAzureCredential")
    def test_get_secret_success(self, mock_credential: MagicMock, mock_client_class: MagicMock) -> None:
        """Test successful secret retrieval from Azure Key Vault."""
        mock_client = MagicMock()
        mock_secret = MagicMock()
        mock_secret.value = "test-secret-value"
        mock_client.get_secret.return_value = mock_secret
        mock_client_class.return_value = mock_client

        vault = AzureKeyVault(vault_url="https://test.vault.azure.net")
        result = vault.get_secret("my_key")

        assert result == "test-secret-value"
        mock_client.get_secret.assert_called_once_with("my-key")

    @patch("app.core.vault.azure_keyvault.SecretClient")
    @patch("app.core.vault.azure_keyvault.DefaultAzureCredential")
    def test_get_secret_not_found_returns_none(self, mock_credential: MagicMock, mock_client_class: MagicMock) -> None:
        """Test that missing secret returns None."""
        mock_client = MagicMock()
        mock_client.get_secret.side_effect = Exception("Secret not found")
        mock_client_class.return_value = mock_client

        vault = AzureKeyVault(vault_url="https://test.vault.azure.net")
        result = vault.get_secret("missing_key")

        assert result is None

    @patch("app.core.vault.azure_keyvault.SecretClient")
    @patch("app.core.vault.azure_keyvault.DefaultAzureCredential")
    def test_store_secret(self, mock_credential: MagicMock, mock_client_class: MagicMock) -> None:
        """Test storing a secret in Azure Key Vault."""
        mock_client = MagicMock()
        mock_result = MagicMock()
        mock_result.properties.version = "v1"
        mock_client.set_secret.return_value = mock_result
        mock_client_class.return_value = mock_client

        vault = AzureKeyVault(vault_url="https://test.vault.azure.net")
        uri = vault.store_secret("new_key", "new_value")

        assert uri == "azurekv://test/new-key/v1"
        mock_client.set_secret.assert_called_once_with("new-key", "new_value")

    @patch("app.core.vault.azure_keyvault.SecretClient")
    @patch("app.core.vault.azure_keyvault.DefaultAzureCredential")
    def test_ping_success(self, mock_credential: MagicMock, mock_client_class: MagicMock) -> None:
        """Test ping returns True when vault is reachable."""
        mock_client = MagicMock()
        mock_client.list_properties_of_secrets.return_value = iter([])
        mock_client_class.return_value = mock_client

        vault = AzureKeyVault(vault_url="https://test.vault.azure.net")
        assert vault.ping() is True

    @patch("app.core.vault.azure_keyvault.SecretClient")
    @patch("app.core.vault.azure_keyvault.DefaultAzureCredential")
    def test_ping_failure(self, mock_credential: MagicMock, mock_client_class: MagicMock) -> None:
        """Test ping returns False when vault is unreachable."""
        mock_client = MagicMock()
        mock_client.list_properties_of_secrets.side_effect = Exception("Connection failed")
        mock_client_class.return_value = mock_client

        vault = AzureKeyVault(vault_url="https://test.vault.azure.net")
        assert vault.ping() is False

    @patch("app.core.vault.azure_keyvault.SecretClient")
    @patch("app.core.vault.azure_keyvault.DefaultAzureCredential")
    def test_close(self, mock_credential: MagicMock, mock_client_class: MagicMock) -> None:
        """Test closing Azure Key Vault client."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        vault = AzureKeyVault(vault_url="https://test.vault.azure.net")
        vault.close()

        mock_client.close.assert_called_once()

    @patch("app.core.vault.azure_keyvault.SecretClient")
    @patch("app.core.vault.azure_keyvault.DefaultAzureCredential")
    def test_sanitize_key(self, mock_credential: MagicMock, mock_client_class: MagicMock) -> None:
        """Test key sanitization replaces underscores and dots."""
        mock_client = MagicMock()
        mock_secret = MagicMock()
        mock_secret.value = "value"
        mock_client.get_secret.return_value = mock_secret
        mock_client_class.return_value = mock_client

        vault = AzureKeyVault(vault_url="https://test.vault.azure.net")
        vault.get_secret("my_key.name")

        mock_client.get_secret.assert_called_once_with("my-key-name")


@pytest.mark.unit
class TestHashiCorpVault:
    """Tests for the HashiCorpVault implementation."""

    @patch("app.core.vault.hashicorp_vault.hvac.Client")
    def test_init_raises_on_auth_failure(self, mock_client_class: MagicMock) -> None:
        """Test that init raises on authentication failure."""
        mock_client = MagicMock()
        mock_client.is_authenticated.return_value = False
        mock_client_class.return_value = mock_client

        with pytest.raises(ConnectionError, match="authentication failed"):
            HashiCorpVault(addr="http://127.0.0.1:8200", token="bad-token")

    @patch("app.core.vault.hashicorp_vault.hvac.Client")
    def test_get_secret_success(self, mock_client_class: MagicMock) -> None:
        """Test successful secret retrieval from HashiCorp Vault."""
        mock_client = MagicMock()
        mock_client.is_authenticated.return_value = True
        mock_client.secrets.kv.v2.read_secret_version.return_value = {"data": {"data": {"value": "secret-value"}}}
        mock_client_class.return_value = mock_client

        vault = HashiCorpVault(addr="http://127.0.0.1:8200", token="good-token", mount_point="secret")
        result = vault.get_secret("my-key")

        assert result == "secret-value"

    @patch("app.core.vault.hashicorp_vault.hvac.Client")
    def test_get_secret_not_found_returns_none(self, mock_client_class: MagicMock) -> None:
        """Test that missing secret returns None."""
        mock_client = MagicMock()
        mock_client.is_authenticated.return_value = True
        mock_client.secrets.kv.v2.read_secret_version.side_effect = Exception("Not found")
        mock_client_class.return_value = mock_client

        vault = HashiCorpVault(addr="http://127.0.0.1:8200", token="good-token")
        result = vault.get_secret("missing-key")

        assert result is None

    @patch("app.core.vault.hashicorp_vault.hvac.Client")
    def test_store_secret(self, mock_client_class: MagicMock) -> None:
        """Test storing a secret in HashiCorp Vault."""
        mock_client = MagicMock()
        mock_client.is_authenticated.return_value = True
        mock_client.url = "http://127.0.0.1:8200"
        mock_client_class.return_value = mock_client

        vault = HashiCorpVault(addr="http://127.0.0.1:8200", token="good-token")
        uri = vault.store_secret("new-key", "new-value")

        assert "vault://" in uri
        assert "new-key" in uri
        mock_client.secrets.kv.v2.create_or_update_secret.assert_called_once()

    @patch("app.core.vault.hashicorp_vault.hvac.Client")
    def test_ping_success(self, mock_client_class: MagicMock) -> None:
        """Test ping returns True when authenticated."""
        mock_client = MagicMock()
        mock_client.is_authenticated.return_value = True
        mock_client_class.return_value = mock_client

        vault = HashiCorpVault(addr="http://127.0.0.1:8200", token="good-token")
        assert vault.ping() is True

    @patch("app.core.vault.hashicorp_vault.hvac.Client")
    def test_ping_failure(self, mock_client_class: MagicMock) -> None:
        """Test ping returns False on error."""
        mock_client = MagicMock()
        mock_client.is_authenticated.side_effect = [True, Exception("Connection lost")]
        mock_client_class.return_value = mock_client

        vault = HashiCorpVault(addr="http://127.0.0.1:8200", token="good-token")
        assert vault.ping() is False

    @patch("app.core.vault.hashicorp_vault.hvac.Client")
    def test_close_is_noop(self, mock_client_class: MagicMock) -> None:
        """Test that close is a no-op."""
        mock_client = MagicMock()
        mock_client.is_authenticated.return_value = True
        mock_client_class.return_value = mock_client

        vault = HashiCorpVault(addr="http://127.0.0.1:8200", token="good-token")
        vault.close()
