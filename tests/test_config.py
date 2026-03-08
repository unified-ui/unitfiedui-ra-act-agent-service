"""Tests for application configuration."""

import os
from unittest.mock import patch

import pytest
from app.config import Settings


@pytest.mark.unit
class TestSettings:
    """Tests for the Settings class."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        s = Settings(
            _env_file=None,  # type: ignore[call-arg]
        )
        assert s.server_host == "0.0.0.0"
        assert s.server_port == 8086
        assert s.log_level == "info"

    @patch.dict(os.environ, {"APP_VAULT_TYPE": "", "VAULT_TYPE": "azure_keyvault"}, clear=False)
    def test_effective_app_vault_type_fallback(self) -> None:
        """Test that effective_app_vault_type falls back to vault_type."""
        os.environ.pop("APP_VAULT_TYPE", None)
        s = Settings(
            vault_type="azure_keyvault",
            app_vault_type=None,
            _env_file=None,  # type: ignore[call-arg]
        )
        assert s.effective_app_vault_type == "azure_keyvault"

    def test_effective_app_vault_type_override(self) -> None:
        """Test that app_vault_type overrides vault_type."""
        s = Settings(
            vault_type="azure_keyvault",
            app_vault_type="dotenv",
            _env_file=None,  # type: ignore[call-arg]
        )
        assert s.effective_app_vault_type == "dotenv"
